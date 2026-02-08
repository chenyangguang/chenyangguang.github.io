---
lang: en
title: Unity Hub Tutorial: Fix Login Redirect to id.unity.cn Issue
date: 2026-02-07 21:49:00
tags:
  - Unity
  - Unity Hub
  - VPN
  - Tutorial
categories:
  - Tech Tutorial
---

# Unity Hub Tutorial: Fix Login Redirect to id.unity.cn Issue

## Problem Description

When using international Unity Hub, clicking login button automatically redirects to `id.unity.cn` instead of international `id.unity.com`. This prevents normal Unity account login.

### Login Flow Analysis
By observing, the login redirect flow is as follows:
1. Click Unity Hub login button
2. First request `api.unity.cn`
3. Redirect to `id.unity.cn`
4. Jump to China region login page

## Attempted Solutions

### Solution 1: Modify hosts file (❌ Failed)

**Approach**: Modify system hosts file to point `id.unity.cn` and `api.unity.cn` to international server IP.

**Steps**:

#### Get International Domain IP
```bash
# Query api.unity.com IP
nslookup api.unity.com
# Result: 35.236.175.221

# Query id.unity.com IP
nslookup id.unity.com
# Result: 34.144.195.225
```

#### Modify hosts file

**macOS System**:
```bash
# 1. Backup hosts file
sudo cp /etc/hosts /etc/hosts.backup

# 2. Edit hosts file
sudo nano /etc/hosts
```

Add at end of file:
```
35.236.175.221 api.unity.cn
34.144.195.225 id.unity.cn
```

Save and exit, then refresh DNS cache:
```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

**Result**: After modification, reopened Unity Hub, login still redirects to `id.unity.cn`, indicating Unity Hub uses more underlying detection method, not dependent on system DNS resolution.

---

### Solution 2: Switch Unity Hub Region Setting (❌ Invalid)

Attempted to switch to international region in Unity Hub settings, but found no relevant region switching option.

---

## Final Solution: Start Unity Hub Through VPN (✅ Successful)

### Principle Analysis

Unity Hub performs region detection based on user's IP address. If China region IP detected, automatically redirects to China login page. By proxying Unity Hub's network traffic to foreign servers via VPN, can bypass this detection.

### Steps

#### Step 1: Prepare VPN Proxy

Ensure you have VPN service that can access international internet, and start proxy server.

Assume proxy server address is:
- HTTP proxy: `http://127.0.0.1:7890`
- HTTPS proxy: `http://127.0.0.1:7890`

#### Step 2: Start Unity Hub Through Environment Variables

**macOS System**:

Open terminal, enter:
```bash
# Set proxy environment variables
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# Start Unity Hub
/Applications/Unity\ Hub.app/Contents/MacOS/Unity\ Hub
```

**Or create a startup script**:

1. Create startup script file:
```bash
nano ~/launch-unity-hub.sh
```

2. Enter:
```bash
#!/bin/bash

# Set proxy environment variables (modify port according to your VPN config)
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# Start Unity Hub
/Applications/Unity\ Hub.app/Contents/MacOS/Unity\ Hub
```

3. Save and exit (Ctrl+O save, Enter confirm, Ctrl+X exit)

4. Add execute permission:
```bash
chmod +x ~/launch-unity-hub.sh
```

5. Later when starting Unity Hub just run:
```bash
~/launch-unity-hub.sh
```

#### Step 3: Verify Login

After starting Unity Hub, click login button, should now redirect to international login page `id.unity.com`, can login normally.

### Windows System Reference

**Windows Command Line**:
```cmd
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
"C:\Program Files\Unity Hub\Unity Hub.exe"
```

**Windows Batch Script**:
Create file `launch-unity-hub.bat`:
```batch
@echo off
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
"C:\Program Files\Unity Hub\Unity Hub.exe"
```

---

## Other Possible Solutions (Not Tested)

### Solution 3: Use Old Unity Hub

Download Unity Hub version before 2022, when mandatory China region detection didn't exist.

Download: [Unity Hub Previous Releases](https://unity.com/releases/hub/previous)

### Solution 4: Command Line Direct Activation of Unity Editor

If have Unity Pro subscription, can use command line to activate Unity Editor, completely bypassing Unity Hub:

```bash
# First need to get activation file from Unity website
# Then activate with command line:
/Applications/Unity/Unity.app/Contents/MacOS/Unity -quit -batchmode -nographics -manualLicenseFile <license_file_path>
```

### Solution 5: Offline Activation (Pro Version Only)

Unity Personal version doesn't support offline activation, only Pro/Enterprise versions.

Reference: [Unity Manual License Activation](https://docs.unity3d.com/6000.3/Documentation/Manual/ManualActivationGuide.html)

---

## Summary

| Solution | Difficulty | Effectiveness | Recommendation |
|----------|-----------|---------------|----------------|
| Modify hosts file | Low | ❌ Invalid | ⭐ |
| Unity Hub region settings | Low | ❌ Invalid | ⭐ |
| **VPN + Environment Variable Start** | Medium | ✅ Effective | ⭐⭐⭐⭐⭐ |
| Use old Unity Hub | Medium | ✅ Possibly Effective | ⭐⭐⭐⭐ |
| Command line activation | High | ✅ Effective | ⭐⭐⭐ |

**Best Practice**: Recommend using VPN + environment variable to start Unity Hub, simple and effective without needing to download other versions.

## FAQ

**Q: Why hosts file modification invalid?**
A: Unity Hub uses more underlying network detection method, not dependent on system DNS resolution, so hosts file cannot take effect.

**Q: Need to set environment variables every time I start?**
A: Yes, or you can add environment variables to system config file (like `~/.zshrc` or `~/.bash_profile`), or use the created startup script.

**Q: Does VPN need to stay on?**
A: Can close VPN after login, but next login needs to start Unity Hub through VPN again.

**Q: Does this affect Unity Editor usage?**
A: No, only affects Unity Hub login process. After successful login, Unity Editor can be used normally, not affected by VPN.

---

## References

- [Unity License Activation Guide](https://docs.unity3d.com/6000.3/Documentation/Manual/ManualActivationGuide.html)
- [Unity Hub Previous Releases](https://unity.com/releases/hub/previous)
- [Unity Discussions: Trouble signing in, I am redirected to "id.unity.cn"](https://discussions.unity.com/t/trouble-signing-in-i-am-redirected-to-id-unity-cn/875158)
