---
title: Cocos Creator 3.8.8 没有快手小游戏发布平台，怎么把包发出去
date: 2026-08-15
description: "Cocos Creator 3.8.8 的构建平台列表里没有快手小游戏。本文记录一条已跑通的出包路线：用微信小游戏导出入口出包，靠快手开发者工具的「自动适配微信小游戏」拉起引擎，并说明这套方案成立的两个前提、客户端探测顺序的坑，以及服务端和后台侧要跟着改什么。"
tags: [Cocos Creator, 快手小游戏, 小游戏, 跨平台, 踩坑]
categories:
---

# Cocos Creator 3.8.8 没有快手小游戏发布平台，怎么把包发出去

> 一个已经发布到微信、抖音小游戏的 Cocos 项目，要再上快手。结果发现 Cocos Creator 3.8.8 的构建平台里根本没有快手这一项。本文记录一条已经跑通真机的出包路线，以及这套方案能成立的前提——它比「怎么出包」更重要。

<!-- more -->

## 一、先确认「不支持」不是错觉

Cocos Creator 3.8.8 构建面板的发布平台下拉里，小游戏这一档有微信、字节跳动（抖音）、支付宝、淘宝、百度、小米快游戏、OPPO、vivo、华为快游戏、荣耀、咪咕……**没有快手**。

不放心的话可以直接翻编辑器的 asar 包，搜 `kuaishou` / `kwai`，同样搜不到平台声明。也就是说，既没有内置平台，也没有官方发布插件可装。

这一步之所以要确认，是因为「找不到平台名」和「平台名我不知道叫什么」是两件事。当时因为查不到可用的 CLI 平台名，构建配置一直没提交，导致快手 AppID 都拿到了却出不了包——**卡住的不是权限，是根本没有入口**。

## 二、官方给的路子：借微信小游戏的壳

快手官方的《快手小游戏导出指南》里写得很直白：各引擎目前都还没上线快手专用导出入口，做法是——

1. 用**微信小游戏**的导出入口出包；
2. 在**快手小游戏开发者工具**里导入这个包，打开「自动适配微信小游戏」（右上角设置 → 本地配置）。

这个开关做的事，本质上只有一行：它会生成一个 `kwaiadapter.js`，内容是

```javascript
GameGlobal.wx = ks;
```

把快手的全局对象 `ks` 挂成 `wx`。引擎侧的小游戏适配层以为自己跑在微信里，照常调 `wx.*`，实际打到的是快手的实现。

理解到这一层，剩下的事情就清楚了：**这是一次全局对象层面的鸠占鹊巢**，所有的坑都出在「谁以为自己是微信」这件事上。

## 三、可复现的 CLI 构建配置

编辑器构建面板有个隐性问题：AppID 靠面板的「上次配置」合并，换台机器或清一次缓存就丢。三端并行发布的时候，这种不可复现的配置迟早出事，所以配置钉进仓库、走 CLI 构建：

```json
// client/build-configs/kuaishou.json
{
  "platform": "wechatgame",
  "debug": false,
  "outputName": "kuaishou",
  "packages": {
    "wechatgame": {
      "appid": "ksXXXXXXXXXXXXXXXXXX"
    }
  }
}
```

三处要点：

- `platform` 声明的是 `wechatgame`——这就是上一节那条路线在构建配置里的样子；
- `outputName` 改成 `kuaishou`，输出到 `build/kuaishou`，**不要覆盖微信的正式包**。默认情况下两次构建会写进同一个目录，微信包被快手 AppID 污染是很难查的一类事故；
- `appid` 填快手的（`ks` 开头那串）。它只会被写进 `project.config.json`；快手开发者工具导入工程时**还要再填一次** AppID，两边都得对。

构建命令：

```bash
CC=/Applications/Cocos/Creator/3.8.8/CocosCreator.app/Contents/MacOS/CocosCreator

$CC --project client --build "configPath=$PWD/client/build-configs/wechatgame.json"
$CC --project client --build "configPath=$PWD/client/build-configs/bytedance-mini-game.json"
$CC --project client --build "configPath=$PWD/client/build-configs/kuaishou.json"
```

顺手记一个 3.8.8 的 CLI 行为：`configPath` 是**按进程启动时的工作目录**解析的，不是按 `--project` 解析。从仓库根目录跑、写相对路径会报「配置不存在」，看起来像文件写错了其实是路径基准不同。显式传绝对路径，别赌。

`debug` 一定给 `false`。调试模式那个左下角的 FPS/DrawCall 面板是引擎 profiler，真机上会盖住底部按钮，在提审截图里尤其难看。

## 四、这套方案成立的两个前提

出包只是开始。借壳能跑起来，靠的是两层各行其是，**改动前必须确认这两点还成立**：

### 前提一：引擎适配层必须能拿到 `wx`

构建产物的 `web-adapter.js` 里有四十来处 `wx.` 调用。如果在快手开发者工具里没开「自动适配微信小游戏」，`wx` 就是 undefined，引擎在启动阶段直接崩，连第一帧都渲不出来。

也就是说，这条路线的可用性完全挂在那个开关上，它不是「优化项」，是**运行前提**。

### 前提二：业务层必须仍然认得出自己在快手

这是整件事里最容易翻车的地方。适配器把 `wx` 指向了 `ks`，如果业务代码还按老顺序「先看有没有 `wx`」来判断平台，就会把快手判成微信——然后拿**快手的 login code** 去调**微信的 code2session**，用错 AppSecret，登录链路整个报废。而且它坏得很隐蔽：编辑器预览、微信真机都正常，只有快手上登不进去。

所以平台探测必须让更专属的全局对象排在前面：

```typescript
export function detectMiniGame(): DetectedMiniGame | null {
    const g = globalThis as Record<string, unknown>;

    // 顺序有讲究：抖音环境里 `tt` 一定存在，个别版本为兼容还会挂个残缺的 `wx`；
    // 快手新接口挂在 `ks`，早期的 `kwaigame` 仍兼容。
    // 认错平台会导致 code2session 拿错 AppSecret，所以先认专属对象，最后才兜微信。
    const tt = g.tt as MiniGameApi | undefined;
    if (tt && typeof tt.login === 'function') return { vendor: 'douyin', api: tt };

    const ks = (g.ks ?? g.kwaigame) as MiniGameApi | undefined;
    if (ks && typeof ks.login === 'function') return { vendor: 'kuaishou', api: ks };

    const wx = g.wx as MiniGameApi | undefined;
    if (wx && typeof wx.login === 'function') return { vendor: 'wechat', api: wx };

    return null;
}
```

两个细节：

- 用 `globalThis[...]` 取，别直接写裸标识符 `wx`。直接写的话，在没有这个全局的环境（Cocos 预览、vitest）里，模块求值阶段就 `ReferenceError`，连开发环境的 mock 实现都进不去。
- 光判存在不够，还要 `typeof x.login === 'function'`。宿主为了兼容挂的那些残缺对象，就是靠这一条筛掉的。

这种「顺序即正确性」的代码，注释救不了它，得有测试钉住：

```typescript
it('识别快手 ks 全局对象', () => {
    const kuaishou = api();
    globals.ks = kuaishou;
    expect(detectMiniGame()).toEqual({ vendor: 'kuaishou', api: kuaishou });
});

it('兼容快手早期 kwaigame 全局对象', () => { /* ... */ });

it('抖音优先级高于兼容 wx 对象', () => {
    const douyin = api();
    globals.tt = douyin;
    globals.wx = api();
    expect(detectMiniGame()).toEqual({ vendor: 'douyin', api: douyin });
});
```

再补一条工程约定：**业务代码里出现 `wx.` / `tt.` / `ks.` 一律视为违规**，全部收敛进适配层的一个文件。三端并行的时候，这条约定的价值不在「整洁」，在于平台判定只有一处、错也只错一处。

## 五、服务端跟着要改什么

客户端认对了平台，只是把正确的 `platform` 字段发了出去。服务端这边有三处要动：

**1）多一个平台的 code2session。** 三家的接口和响应形状都不一样，成功/失败的判定条件也不同：

| 平台 | 接口 | 成功字段 | 失败字段 |
| --- | --- | --- | --- |
| 微信 | `jscode2session` | `openid` | `errcode`（成功时缺省或 0） |
| 抖音 | `jscode2session` v2 | `data.openid` | `err_no` |
| 快手 | `auth.code2Session` | `open_id` | `result` / `error_code` / `error_msg` |

快手的响应解释起来要小心，成功不是「没有错误码」而是「有 `open_id`」：

```rust
fn interpret(body: KuaishouSession) -> Result<OpenId, AuthError> {
    if let Some(open_id) = body.open_id {
        return Ok(OpenId::new(open_id));
    }
    // 没有 open_id 又没有可用错误码，说明响应结构不对，不能当成「code 无效」吞掉
    let errcode = body.error_code.or(body.result);
    match errcode {
        Some(0 | 1) | None => Err(AuthError::MalformedResponse),
        Some(errcode) => Err(AuthError::CodeRejected { errcode }),
    }
}
```

把「平台拒绝了这个 code」（客户端问题，401）和「平台响应不对劲」（我们和平台之间的问题，5xx）分成两种错误，线上排查时省的时间远超写这几行的成本。

**2）平台枚举加值。** 数据库里 `platform` 是个枚举，加一条迁移：

```sql
-- 增加快手小游戏平台来源
ALTER TYPE platform ADD VALUE 'kuaishou';
```

**3）凭据按平台隔离。** `KUAISHOU_APP_ID` / `KUAISHOU_APP_SECRET` 走环境变量，AppSecret 绝不进 git、不进日志、不进 `Debug` 输出（`Debug` 手写掩码，别让它跟着 `AppState` 一起被打印出来）。AppID 随包公开分发不算机密，可以入库。

生产环境还加了一条：**缺任何一个平台的凭据就拒绝启动**。否则最坏的情况是悄悄退回开发用的 mock 实现——那意味着任意 code 都能登录成功。

## 六、验收清单

借壳出来的包，不能只看「能启动」。这几项是真出过问题或真值得复验的：

- **分包还在不在。** 项目把笔画数据切成了独立 Bundle 走微信/抖音的分包。因为快手包实际是微信包，分包策略是复用的，但仍然要打开产物的 `game.json` 确认 `subpackages` 条目还在——主包超限是提审阶段最浪费时间的一类退回。实测主包 3.1MB、数据分包 1.7MB，在 4MB 限内。
- **横竖屏设置**是否跟着配置走。
- **真机预览**：用后台生成的 `kwai://` 二维码在快手 APP 里跑，开发者工具里正常不代表真机正常。
- **登录链路没退回 mock**：拿一个假 code 打 `/v1/auth/login`，**必须返回 401 而不是 200**。返回 200 说明服务端在用假实现，这时候所有「登录成功」的截图都是假的。

## 七、后台侧几个能省半天的坑

出包之外，快手后台这一侧也有几处反直觉的地方：

- **AppSecret 那个输入框默认显示的是占位符**，一串 22 个 0，不是你的密钥。要点旁边的眼睛图标才会去拉真值。更坑的是这个按钮用脚本 `element.click()` 触发不了（框架的事件处理器不监听合成的 click），要老老实实模拟 `mousedown` → `mouseup` → `click` 三连——用自动化脚本抓配置的话，这里会静默拿到 22 个 0 然后写进生产环境。
- **凭据写进生产前先验一次**：拿 `app_id` + `app_secret` + 一个乱填的 `js_code` 去打 code2session，返回「Invalid jscode」说明**密钥是对的**（只是 code 假），返回「Invalid app secret」才是密钥错了。界面上读到的值不等于真值，这一步只花一分钟。
- **创建审核通过前，服务器域名怎么填都报错**。提交合法域名恒返回一个固定错误码，那是应用状态导致的，跟你填什么无关，别在这上面反复试。
- **包体上传只能在快手小游戏开发者工具里点**，网页后台没有这个入口。创建审核没过之前上传会报「无此游戏」，审核通过后自动解除。
- **主体资格**：快手小游戏文档明确只支持企业主体入驻，个人主体走不通——这跟微信、抖音都不一样。如果软著权利人是自然人而接入主体是公司，上线时还要补一份授权书。这条最好在立项时就确认，不然客户端都做完了才发现主体不对，很被动。

## 小结

一句话版本：**Cocos Creator 3.8.8 不支持快手，官方解法是借微信小游戏的壳出包，靠快手开发者工具把 `wx` 指向 `ks` 拉起引擎。**

但真正需要写进项目文档的是那两个前提：引擎层依赖 `wx` 存在，业务层必须先认 `ks`。这两条一旦被后来的改动打破，症状分别是「白屏起不来」和「只有快手登不上」——都不便宜。

最后，这条路线是引擎侧还没上线快手导出入口时的过渡方案，是否已有官方平台支持，请以你手上的 Cocos 版本和快手当前文档为准。
