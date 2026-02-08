---
lang: en
title: Your Time to Be Tested Has Arrived
date: 2018-12-02
description: 'Weekend Release Saturday launch, major version upgrade. Although not too much fluctuation, it was still full of twists and turns. Let me make a record. There are certainly many areas for improvement. Yesterday I was thinking of summarizing. But yesterday other departments tossed until 22:00+. Got home at 11:30, didn't have time to review carefully. Washed and slept. Today let me review what launch operation techniques were used. In Position 8:30 I was already in position. Basically entered the launch rhythm. But the four other departments launching at the same time weren't ready yet. I need to wait for one department's person to send大概几十万 initialization data related to this requirement, for initialization.'
tags: [Computer Technology]
categories:
---

[](#Weekend-Release)Weekend Release
Saturday launch, major version upgrade. Although not too much fluctuation, it was still full of twists and turns. Let me make a record. There are certainly many areas for improvement.
Yesterday I was thinking of summarizing. But yesterday other departments tossed until 22:00+. Got home at 11:30, didn't have time to review carefully. Washed and slept.
Today let me review what launch operation techniques were used.

[](#In-Position)In Position
8:30 I was already in position. Basically entered the launch rhythm. But the four other departments launching at the same time weren't ready yet. I need to wait for one department's person to send大概几十万 initialization data related to this requirement, for initialization.
So I wrote the launch documentation, reorganized the source code logic and flow of this development. Confirming it ran smoothly once. Ran the backend unit test go test once. Confirming no problems in development and test environments.

[](#Preparation)Preparation
9:00 Started refining the documentation discussed and modified with the architect the day before (Friday), including data initialization changes. Originally Friday afternoon I was preparing to close the dev-feature feature branch to be launched. But after the architect reviewed it. He thought my initialization data had some problems. Mainly the initialization wasn't thorough enough, leaving a few residues not initialized. So I modified two versions of the plan. Among them, the initialization of industry and address dictionary parts, I changed from the original upload file script modification to importing a temporary table, then using join queries, batch updating based on different conditions.
Waiting for the initialization data, kept urging them, still didn't get the formal line initialization data.
So before getting the initialization data at 15:30, I did these things in sequence:

Removed irrelevant code comments, redundant log prints.
Merged frontend code, submitted to version repository. Because need to pull the node_module directory, prepared the frontend code image in advance.

Merged backend go code, submitted to version repository pending release branch.

1
2
3
4
5
6
7
git checkout master
git fetch
git checkout dev-feature
git rebase  master -i
# Then keep one feature point commit, modify other commits to squash
# This ensures the master trunk remains clean, equivalent to this 100 commits merging into one commit

Refined the launch documentation again.

Listed every database table change operation SQL to be executed in execution order, according to four function blocks. Refined to every single SQL, including pre-change queries and post-change confirmation SQL all added.
Initially listed modification points 1-7. Before launch, had the architect review again. Architect confirmed no errors.
Added detailed description of monitoring integration.
Confirmed the docker cluster IP to deploy to.

In advance, configured the relevant domain names of the configuration server, opened ports, various sensitive parameters, signatures.
Configured the online open API. Published, applied for review and passed, then proceeded with corresponding business line authorization.

[](#Initialization)Initialization
Before all database operations, backup first.

```stylus
mysqldump -uroot -p dbname table_name > table_xxx_20181201.sql
```

16:00 Finally, after a thousand calls, the initialization data arrived. I followed my documentation in sequence. Executed the initialization. When I first received the initialization file, I thought of using **rsync** to upload the file. But it didn't work. Changed to **rz** to synchronize the initialization data file to the server. Then planned to import directly from the terminal.

```stylus
mysqldump -uroot -p db_name 1
2
3
4
5
6
ALTER TABLE X ADD COLUMN xxx VARCHAR(50) NOT NULL COMMENT 'XXX';
UPDATE TABLE ...
ALTER TABLE ADD INDEX (`YYY`);
...
# There's a whole bunch of operations, follow the process documentation.

Initialization took about 30 minutes.
By now it's around 16:30! According to the launch order, I can only launch after all three other departments have finished launching. But one of the departments is still initializing.
Then continued waiting. As a result, waited until nearly 20:00 in the evening, finally got the news: other departments' initialization was complete, now I could launch. In the meantime, I also added monitoring items to all the incoming and outgoing interfaces integrated this time. This way, once the code launched, I could start watching logs while watching monitoring to discover existing problems.

[](#Launch)Launch
So I used 7 seconds to deploy all backend images. Why? Because while waiting for other departments to operate, I had all the images prepared. Everything was ready, only needed Thanos's snap. Oh, seems something's wrong.
Immediately followed by launching frontend containers.
Watched logs, found one error level. Feedback was that a database field couldn't be found! This field was modified in version 8! Quickly added it. After this, that error level log disappeared in subsequent time.
Then联合线上回归. Found several more problems. Immediately followed up!
Turned out one of the problems was on my side, a table's time field set as int(11) didn't have UNSIGNED! Not enough length. So I modified this field's length.

```sql
ALTER TABLE table_name CHANGE `x_column` `x_column` int(11)  UNSIGNED  NOT NULL DEFAULT 0 COMMENT 'Expiration time';
```

Then verified, still not enough. Turned out another interface returned timestamp accurate to millisecond level, expanding from 2147483647 to 4294967295 still wasn't enough. So I changed it to bigint and it worked.
Other problems, assisted them in verifying online bugs for log follow-up. Resolved them one by one.

After verification, it was already 22:00.
Then took the subway home!

[](#Summary)Summary
Always be prepared to handle any anomalous issues from the production environment. Production environment and test environment can't be completely identical, can only infinitely approach.
Write as many unit tests as you can, add stress testing where necessary.
Operation process must be clear.
Must have a global view.
Response must always remain fast enough.
