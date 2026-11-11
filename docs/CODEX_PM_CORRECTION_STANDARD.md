# Career DNA Studio：Codex 产出改正规范

状态：本文件是下一轮 PM 专项改版的执行与验收标准。用户最新要求优先于之前“通用职业分类”方案。素材包已包含 24 个人物和 24 个 PM 图标；它们是内部素材，不是 24 份用户结果。除文末注明的双图修复外，本规范中的角色、主题和人物库选择尚待 Codex 接入网站。

## P0 — 每次只产出一份 My Career DNA

1. 页面只存在一个可见的最终结果根节点，只有一张完整的 My Career DNA 地图。
2. 地图内部包含 My Career Journey 与 Shape My Career DNA 两个部分。这是同一张图的两个部分，不是上下两张完整地图。
3. 生成、重新生成、窗口缩放、下载、打开证据后，结果仍只有一份。重新生成使用替换，不能 append 新地图、保留旧预览或同时渲染两套桌面/手机结果。
4. 只提供一个 Download PNG。一次点击只触发一次下载事件和一个 PNG 文件。不得附带第二张图、备选稿、人物图集或对照图。
5. 下载图片与当前结果使用同一份内容、人物 ID、主题 ID、图标 ID 和排版版本，不得在导出时重新抽签。
6. 导出 canvas 必须用 `document.createElement('canvas')` 创建，并且永远不 append 到 DOM。不能只依赖 hidden、透明度或负坐标来隐藏第二张完整图。
7. 删除旧的全局 canvas 显示样式；对其他隐藏控件使用 `[hidden] { display:none !important; }`。
8. **已查明的真实双图原因**：原页面的 `canvas[hidden]` 被 `canvas { display:block }` 覆盖，使 SVG 预览与 PNG 导出画布同时可见。之前只数 SVG 的测试不充分。必须同时检查 SVG、canvas、img、背景图、重复组件和 portal 的实际可见性。

验收：可见完整结果数量 = 1；结果区域 DOM 导出 canvas 数量 = 0；下载事件数量 = 1。不能以“只有一个 SVG”代替这个验收。

## P0 — 任何前景内容不得互相遮挡

- 为人物、每个职业图标、角色标题、摘要、岛屿、能力图标、能力标题和能力说明定义独立的占位框。
- 在 1600px 宽的设计坐标中：图标到标题至少 16px；标题到摘要至少 12px；相邻前景内容安全框至少 20px；卡片内边距至少 24px。
- 人物整体（含头发、手、背包、笔记本和自带道具）必须完全位于人物区。不得让卡片压到人物，或让额外职业图标叠在笔记本、脸、手或其他图标上。
- 不要再为人物额外叠加一个会遮挡人物/笔记本的贴纸图标；优先选择本身就带合适道具的人物素材。
- 岛屿顶部、职业图标、文字、连接箭头各有独立垂直区域。文字不可印在图标、岩石、植物或发光路径上。
- 花草、云朵、光晕只能进入背景装饰区，不能进入文字/图标/人物的安全框。路径位于前景内容后方，不能降低文字对比度。
- 图集裁切不能带入相邻格子的碎片。每个 sprite 必须使用 manifest 的边界并经过透明边缘检查。
- 长文字先请求 AI 缩写为完整短句，再重新排版；不得叠放、裁字、挤到边框外，或缩小到不可读。
- 下载图的正文在 1600px 设计宽度下建议至少 20px；手机实际显示正文至少 14 CSS px。超过排版容量时阻止下载并让内容修复。
- 可以有参考图风格的阴影、透明面板与背景光晕层叠，但**不能有语义前景元素之间的遮挡**。

验收：为语义前景框运行相交检测。32 种独立 1–4 角色 × 1–4 能力 × 桌面/手机布局均不得碰撞。另测最长合法文本、字体加载完成后、缩放及实际 PNG。截图人工检查不能由纯计数测试替代。

## P1 — 产品聚焦互联网产品经理

### 上层：经历中的 PM 角色类型

上层回答“你做过哪些类型的产品角色”，不是“你会什么”。名称以 PM 功能类型为主，保留真实职责和原始职位的证据。

优先角色：Growth PM、Platform PM、Operations PM、AI PM、Data PM、Consumer PM、B2B / Enterprise PM、Commerce PM、Marketplace PM、Monetization PM、Content PM、Trust & Safety PM、Technical PM、UX PM、AI Enablement PM。

- Growth Hacker 是用户明确提供的真实经历时，可以显示 Growth Hacker / Growth，不能自动把非 PM 职位改成 Growth PM。
- Product Operations 与 Operations PM 不能因名字相似而混同：需要产品职责证据，保留 source_role_title。
- AI PM 需要产品问题定义、产品决策/交付等证据；参与模型评估本身不等于担任 AI PM。
- 历史非 PM 工作可以作为支持能力的背景；没有 PM 角色证据时问一个聚焦问题。不能把工程师、运营专员或咨询顾问自动升级成 PM。
- 不在上层使用 Product Development、Business Consulting、Multimodal Evaluation、LLM Evaluation Pipeline、Prompt Baselines 等笼统领域、能力或项目任务作为 PM 角色类型。
- AI Product Management 统一成用户容易理解的角色标签 AI PM；下层能力可以是 AI Product Judgement。两者不能混写。
- 1–4 个角色节点，依证据独立决定。相邻同类角色合并，详情保留原始经历；不能为了四个岛屿虚构职业转型。没有可靠日期时不要画方向性的晋升/转型箭头。

### 两张参考图的角色语言

`references/pm-archetypes-reference.png` 的六种表达是 The Growth Hacker、The System Architect、The AI Translator、The Risk Guardian、The Enterprise Solver、The AI Enablement Builder。对应功能类型分别为 Growth、Platform、AI、Trust & Safety、B2B / Enterprise、AI Enablement；Operations PM 是用户另行指定的角色。

这些创意 archetype 名字用于角色风格与能力归纳的参考，不能伪造为用户实际职位，也不能把图中的“obsessed”“别人看不到的风险”等宣传句直接当作用户人格/能力结论。`references/my-product-dna-reference.png` 决定整张图的双层构图；archetypes 图补充角色、道具、色彩语言。不要把六宫格参考图当成第二张用户结果。

### 下层：经历共同塑造的可迁移能力

下层回答“这些经历使你形成了什么能力”。不是第二遍复述角色或抄项目关键词。

| 经历角色（有证据才显示） | 可支持的能力例子（仍须逐项有证据） |
| --- | --- |
| Growth PM / Growth Hacker | Growth Experimentation、Data-Informed Decisions、User Insight |
| Platform PM | Systems & Platform Design、Scalable Product Thinking |
| Operations PM | Workflow Design、Stakeholder Coordination、Operational Judgement |
| AI PM | AI Product Judgement、Evaluation Strategy、Human-AI Interaction |
| Trust & Safety PM | Risk & Trust by Design、Policy-to-Product Translation |
| Marketplace PM | Ecosystem Thinking、Incentive Design、Commercial Problem Solving |

映射不是自动授予能力。例：没有实验设计证据就不能因为 Growth PM 标签自动生成 Experimentation；没有领导范围就不能默认 Cross-Functional Leadership。

能力独立为 1–4 项，不与角色数量绑定。禁止把 Growth PM、Platform PM、AI PM 再当能力卡标题。每个能力给一条简短解释，并关联支持它的角色 ID、原文证据片段和来源 ID。

## P1 — 多种配色，但只有一个固定构图系统

- 使用 `themes.json` 中的 6 套批准配色：蓝、薄荷绿、暖黄、珊瑚桃、青绿、浅紫。地图不能每次都使用紫色底。
- 紫色仅为其中一套主题；正常主题抽样中占比不高于 1/6。保留品牌按钮的紫色不等于所有结果背景都紫色。
- 每张地图仍使用一套主背景与 3–4 个协调辅色，不给每个元素随机乱配色。
- 同一图中的文字统一深色，保持至少 4.5:1 的正文对比度。不能用颜色表示能力高低或人格判断。
- 新生成可选择新的主题；同一份结果在 resize、导出、展开证据时必须保持 theme_id 不变。
- 主题变化只影响批准颜色与装饰色，不能改变岛屿、人物、卡片的 3D 画风或整体层级。

## P1 — 24 人物与 24 PM 图标的可复用库

使用 `assets/pm-characters-24.png` 与 `assets/pm-icons-24.png`。每张图集为 1536×1024、6 列×4 行、单格 256×256。`manifest.json` 为每格提供稳定 ID 与源坐标。**图集是内部调用素材，绝不能作为用户的 Career DNA 结果显示。**

人物：统一的高质量 3D 人物 Q 版；大头小身、亲切表情、产品工作道具。24 个形象有不同发型、服装色、眼镜、肤色、姿势与道具。全部是虚构品牌人物，不能声称是用户肖像。

选择：以当前会话随机种子和工作道具匹配选择 avatar_id；不要从姓名、CV、语言、国家、性别、年龄、种族等推断外貌。不得把某种肤色固定映射某类 PM。新生成应避免紧接着重复同一个人物；同一结果的预览、缩放、导出必须复用相同 avatar_id。

图标：24 种图标涵盖增长、漏斗、平台、API、运营、AI、分析、实验、信任安全、用户洞察、战略、路线图、UX、电商、移动端、SaaS、企业产品、内容、市场平台、推荐、商业化、协作、交付和自动化。只能调用存在的 icon_id，不允许模型提供 SVG 代码、图片 URL 或任意图标。

素材质量：当前图集原生单格 256px，适合约 220 CSS px 内的人物/图标显示。更大的精细高清人物需要后续单独生成/精修高分辨率母图；不能将简单插值放大称为新增高清细节。上线前检查每格轮廓、透明边缘、裁切和主体安全边距；不合格素材不得硬接入。

## 架构与建议数据结构

Stage A：大模型只负责抽取、归纳和引用，不负责自由生成整张图。

```json
{
  "title": "My Career DNA",
  "roles": [{
    "id": "r1",
    "role_type": "platform_pm",
    "role_label": "Platform PM",
    "source_role_title": "actual title from source",
    "period": null,
    "summary": "Reusable capabilities for product teams",
    "icon_id": "pm_icon_03",
    "evidence_refs": ["source_1"],
    "evidence_passage_ids": ["source_1_p3"]
  }],
  "capabilities": [{
    "id": "c1",
    "label": "Systems & Platform Design",
    "explanation": "Connects shared capabilities into scalable products",
    "role_ids": ["r1"],
    "evidence_passage_ids": ["source_1_p3"]
  }],
  "render_variant": {
    "template_version": "pm-world-v2",
    "theme_id": "sky_blue",
    "avatar_id": "pm_avatar_04"
  }
}
```

这是目标结构，Codex 可兼容现有 schema，但必须保持角色、能力、渲染元数据分离。`render_variant` 在生成完成时只选一次。随机种子不使用持久 CV 哈希，不引入个人追踪。

Stage B：调用固定组件与本地素材库组装一张图，使用真实 HTML/SVG 文字。导出来自同一内容对象和固定 variant，不再次请求模型生成图片。人物/图标 PNG 不包含用户简历；最终下载不嵌入原文、姓名、联系人、source_id、证据引用或素材图集。

## 必须保留的功能与边界

- 多语言输入，最终地图文字仅英文；原文证据可在只读 View Full Journey 中保留原语言。
- 上传/语音/文字输入、明确 loading、错误后保留输入、回原框重新生成、单个 PNG 下载。
- 保留逐字证据配对、安全检查、1–4 独立边界、不编造职位与能力、不填满槽位。
- 不重新加入手动改图、独立 Make It Yours、格式选择或多个结果候选。
- 不存储简历、故事、录音转写、地图或访问者身份；保留现有聚合次数。不要新增个人追踪。
- 调用限额与已配置的服务端密钥保持不变。20 次/天是观察目标，不是提高调用上限的授权。

## 最终交付门槛

- [ ] 可见完整 My Career DNA 数量为 1；DOM 内没有导出画布；点击 Download 只得到一个文件。
- [ ] 重新生成和手机/桌面切换后仍只有一份。
- [ ] 文字、职业图标、人物、道具、岛屿与相邻卡片通过前景安全框相交检测。
- [ ] 用户 PM 经历被映射为真实 PM 角色类型，而非项目、能力或无关通用职业领域。
- [ ] 下层是独立、有证据的能力，而非角色标题重复。
- [ ] 六主题库确实应用到地图背景，非只替换按钮色。
- [ ] 24 人物与 PM 图标按 ID 调用；同一结果导出不换人、不换色。
- [ ] 截取完整页面与下载 PNG；与两张原始参考图对照，确认没有机器人、平面图标替代或丢失装饰环境。
- [ ] 检查稀疏/丰富输入、最长文本、1–4 独立数量、手机与桌面、连续两次生成、错误重试和下载。
- [ ] 未通过任一 P0 项不得宣称完成，不得只报告“测试通过”而跳过视觉检查。

## 本次已实施的紧急修复

当前项目已将导出 canvas 改为脱离 DOM 的对象，并删除导致 hidden 被覆盖的全局 canvas 显示样式。浏览器回归测试同时检查唯一 SVG 与“结果区 DOM canvas = 0”。PM 分类、主题抽样和 24 人物/图标库接入是下一轮按此规范执行的工作，不能因交付了本文件就宣称已全部上线。
