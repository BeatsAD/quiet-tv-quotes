# Quiet TV 每日格言

Quiet TV 的公开格言源。中国古代、外国古典、中国近现代、外国近现代四类交替，每条显示简体中文和出处。第一批 120 条覆盖 2026-11-24 至 2027-03-23。

## 数据与部署

GitHub Pages 从 `main` 的 `docs/` 发布。以设备的本地日期读取 `daily/YYYY-MM-DD.json`。

- [站点首页](https://beatsad.github.io/quiet-tv-quotes/)
- [首日接口示例](https://beatsad.github.io/quiet-tv-quotes/daily/2026-11-24.json)
- [格言、原文及权利状态](catalog.json)

每个响应包含 `date`、`text`、`credit`。有额外署名义务的条目同时提供 `source`、`license` 和 `adaptation`。日期文件预先提交，内容更新随分支部署。

补充格言时，在 `catalog.json` 中追加每类相同数量的条目，保留现有条目在所属分类中的次序。通过以下命令生成并核对连续日期文件。

```sh
python3 build_feed.py
python3 build_feed.py --check
```

## 授权

原文按各来源的公有领域或开放许可标注使用。作品、旧译原文、授权依据和来源链接见 [catalog.json](catalog.json)。本仓库制作的中文译文和原创编排采用 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)。整理脚本也以同一方式提供。第三方署名条目继续适用其注明的许可。

「人生只有一次，不虚度光阴。」引自 YOLO 人生的[关于页](https://www.yolo.blue/about/)，遵循 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。这条内容摘录自原句，调整了句末标点。
