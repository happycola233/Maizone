from maibot_sdk import Field, PluginConfigBase
from pathlib import Path

config_file_path = Path(__file__).parent / "config.toml"


def _ui(label: str, hint: str = "", order: int = 0) -> dict[str, object]:
    """构造 WebUI 配置项中文展示元数据。"""

    schema_extra: dict[str, object] = {"label": label, "order": order}
    if hint:
        schema_extra["hint"] = hint
    return schema_extra


class PluginSectionConfig(PluginConfigBase):
    """插件基础配置。"""

    __ui_label__ = "基础配置"
    __ui_order__ = 0

    enabled: bool = Field(default=True, description="是否启用插件", json_schema_extra=_ui("启用插件", "关闭后 Maizone 不会处理 QQ 空间相关命令和任务。", 0))
    config_version: str = Field(default="1.0.0", description="配置版本", json_schema_extra=_ui("配置版本", "内部配置版本，请勿手动修改。", 1))
    text_model: str = Field(default="replyer", description="[默认即可]使用的文本模型在主程序的任务名（'replyer','planner','embedding', 'emoji', 'learner', 'memory', 'utils', 'vlm', 'voice'）", json_schema_extra=_ui("文本模型任务", "用于生成说说、评论和回复的文本模型任务名，通常保持 replyer 即可。", 2))
    # 获取cookie相关配置
    http_host: str = Field(default="127.0.0.1", description="NapCat HTTP服务地址，仅 cookie_methods 包含 napcat_http 时使用", json_schema_extra=_ui("NapCat HTTP 地址", "仅 cookie_methods 包含 napcat_http 时使用。", 3))
    http_port: int = Field(default=9999, description="NapCat HTTP服务端口，仅 cookie_methods 包含 napcat_http 时使用", json_schema_extra=_ui("NapCat HTTP 端口", "仅 cookie_methods 包含 napcat_http 时使用。", 4))
    napcat_token: str = Field(default="", description="NapCat HTTP服务Token，仅 cookie_methods 包含 napcat_http 时使用", json_schema_extra=_ui("NapCat HTTP Token", "NapCat HTTP 服务的鉴权 Token；未启用鉴权可留空。", 5))
    cookie_methods: list[str] = Field(default=["qrcode", "local"], description="Cookie获取方式（顺序尝试）：qrcode、local；可显式加入snowluma_adapter、napcat_adapter或napcat_http", json_schema_extra=_ui("Cookie 获取方式", "按顺序尝试：qrcode、local、snowluma_adapter、napcat_adapter、napcat_http。", 6))

class SendConfig(PluginConfigBase):
    """指令发说说配置"""

    __ui_label__ = "发说说"
    __ui_order__ = 1

    history_number: int = Field(default=5, description="生成新说说时回顾的历史说说数量", json_schema_extra=_ui("历史说说数量", "生成新说说时参考最近多少条历史说说。", 0))
    # 配图相关配置
    enable_image: bool = Field(default=True, description="是否附带表情包", json_schema_extra=_ui("启用配图", "发布说说时是否尝试附带图片。", 1))
    # 图片模式
    image_mode: str = Field(default="only_emoji", description="图片使用方式: only_ai(仅AI生成)/only_emoji(仅表情包)/random(随机混合)", json_schema_extra=_ui("配图模式", "only_ai=仅 AI 生图；only_emoji=仅表情包；random=随机混合。", 2))
    ai_probability: float = Field(default=0.5, description="random模式下使用ai生图概率", json_schema_extra=_ui("AI 生图概率", "配图模式为 random 时，选择 AI 生图的概率。", 3))
    image_number: int = Field(default=1, description="每条说说附带图片数量", json_schema_extra=_ui("配图数量", "每条说说最多附带的图片数量。", 4))
    # 提示词相关配置
    prompt: str = Field(
        default=(
            "你是'{bot_personality}'，现在是'{current_time}'你想写一条主题是'{topic}'的说说发表在qq空间上，"
            "{bot_expression}，不要刻意突出自身学科背景，不要浮夸，不要夸张修辞，可以适当使用颜文字，只输出一条说说正文的内容，不要输出多余内容"
            "(包括前后缀，冒号和引号，括号()，表情包，at或 @等 )"
        ),
        description="生成说说的提示词，占位符包括{current_time}（当前时间），{bot_personality}（人格），{topic}（说说主题），{bot_expression}（表达方式）",
        json_schema_extra=_ui("生成说说提示词", "控制根据主题生成 QQ 空间说说正文的提示词。", 5),
    )

class ReadConfig(PluginConfigBase):
    """指令读说说配置"""

    __ui_label__ = "读说说"
    __ui_order__ = 2

    # 其它配置
    read_number: int = Field(default=5, description="读取的说说数量", json_schema_extra=_ui("读取说说数量", "每次读取目标 QQ 空间时获取的动态数量。", 0))
    like_probability: float = Field(default=1.0, description="读每条说说后点赞的概率", json_schema_extra=_ui("点赞概率", "读到每条说说后自动点赞的概率，范围建议 0 到 1。", 1))
    comment_probability: float = Field(default=1.0, description="读每条说说后评论的概率", json_schema_extra=_ui("评论概率", "读到每条说说后自动评论的概率，范围建议 0 到 1。", 2))
    # 提示词相关配置
    prompt: str = Field(
        default=(
            "你是'{bot_personality}'，你正在浏览你好友'{target_name}'的QQ空间，你看到了你的好友'{target_name}'"
            "在qq空间上在'{created_time}'发了一条内容是'{content}'的说说，你想要发表你的一条评论，现在是'{current_time}'"
            "你对'{target_name}'的印象是'{impression}'，若与你的印象点相关，可以适当评论相关内容，无关则忽略此印象，"
            "{bot_expression}，回复的平淡一些，简短一些，说中文，不要刻意突出自身学科背景，不要浮夸，不要夸张修辞，不要输出多余内容"
            "(包括前后缀，冒号和引号，括号()，表情包，at或 @等 )。只输出回复内容"
        ),
        description=(
            "对无转发内容说说进行评论的提示词，占位符包括{current_time}（当前时间），{bot_personality}（人格），"
            "{target_name}（说说主人名称），{created_time}（说说发布时间），"
            "{content}（说说内容），{impression}（对说说主人的印象点），{bot_expression}（表达方式）"
        ),
        json_schema_extra=_ui("普通说说评论提示词", "控制读取普通说说后生成评论的提示词。", 3),
    )
    rt_prompt: str = Field(
        default=(
            "你是'{bot_personality}'，你正在浏览你好友'{target_name}'的QQ空间，你看到了你的好友'{target_name}'"
            "在qq空间上在'{created_time}'转发了一条内容为'{rt_con}'的说说，你的好友的评论为'{content}'，你对'{"
            "target_name}'的印象是'{impression}'，若与你的印象点相关，可以适当评论相关内容，无关则忽略此印象，"
            "现在是'{current_time}'，你想要发表你的一条评论，{bot_expression}，"
            "回复的平淡一些，简短一些，说中文，不要刻意突出自身学科背景，不要浮夸，不要夸张修辞，"
            "不要输出多余内容(包括前后缀，冒号和引号，括号()，表情包，at或 @等 )。只输出回复内容"
        ),
        description=(
            "对转发的说说进行评论的提示词，占位符包括{current_time}（当前时间），{bot_personality}（人格），{"
            "target_name}（说说主人名称），{created_time}（说说发布时间），{"
            "content}（说说评论内容），{rt_con}（转发说说内容），{impression}（对说说主人的印象点），{"
            "bot_expression}（表达方式）"
        ),
        json_schema_extra=_ui("转发说说评论提示词", "控制读取转发说说后生成评论的提示词。", 4),
    )

class AutoSendConfig(PluginConfigBase):
    """自动发说说配置"""

    __ui_label__ = "自动发说说"
    __ui_order__ = 3
    
    enable_auto_send: bool = Field(default=False, description="是否自动发说说", json_schema_extra=_ui("启用自动发说说", "开启后按日程和概率自动发布 QQ 空间说说。", 0))
    daily_probability: float = Field(default=0.3, description="每天发说说的概率", json_schema_extra=_ui("每日发送概率", "每天是否自动发说说的概率，范围建议 0 到 1。", 1))
    schedule: list[str] = Field(default=["08:00", "20:00"], description="每天发说说的时间点（24小时制，格式\"HH:MM\"，多个时间点用逗号分隔，如\"08:00,20:00\"）", json_schema_extra=_ui("发送时间点", "每天尝试自动发说说的时间点，格式 HH:MM。", 2))
    fluctuation: int = Field(default=60, description="发说说时间的随机浮动范围（分钟）", json_schema_extra=_ui("时间随机浮动", "自动发说说时间允许前后随机浮动的分钟数。", 3))
    random_topic: bool = Field(default=True, description="是否随机选择说说主题，若关闭则随机使用固定主题", json_schema_extra=_ui("随机主题", "开启后自动生成随机主题；关闭后从固定主题列表中抽取。", 4))
    fixed_topic: list[str] = Field(default=["散文鉴赏", "今天也要加油", "日常碎片", "哲学小谈", "今天吃什么", "看书打卡", "想不到发什么了", "运动健身", "打游戏", "丧文化", "灵感碎片"],
                                   description="固定说说主题列表", json_schema_extra=_ui("固定主题列表", "关闭随机主题时，从这里随机选择说说主题。", 5))

class AutoReadConfig(PluginConfigBase):
    """自动读说说配置"""

    __ui_label__ = "自动读说说"
    __ui_order__ = 4

    # 自动阅读
    enable_auto_read: bool = Field(default=True, description="是否自动读说说", json_schema_extra=_ui("启用自动读说说", "开启后定时读取允许范围内的 QQ 空间动态。", 0))
    interval: int = Field(default=15, description="自动读说说的间隔时间（分钟）", json_schema_extra=_ui("读取间隔", "自动读说说任务的间隔时间，单位分钟。", 1))
    silent_duration: str = Field(default="22:00-07:00", description="不刷空间的时间段（24小时制，格式\"HH:MM-HH:MM\"，多个时间段用逗号分隔，如\"23:00-07:00,12:00-14:00\"）", json_schema_extra=_ui("静默时间段", "这些时间段内不自动刷空间，格式 HH:MM-HH:MM。", 2))

class AutoReplyConfig(PluginConfigBase):
    """自动回复评论配置"""

    __ui_label__ = "自动回评论"
    __ui_order__ = 5

    # 自动回复
    enable_auto_reply: bool = Field(default=True, description="是否在自动读说说时回复自己说说的评论", json_schema_extra=_ui("启用自动回评论", "开启后自动读说说时会尝试回复自己说说下的新评论。", 0))
    reply_number: int = Field(default=5, description="自动回复的最新说说数量", json_schema_extra=_ui("检查说说数量", "自动回复评论时检查自己最近多少条说说。", 1))
    reply_probability: float = Field(default=1.0, description="对每条评论的回复概率", json_schema_extra=_ui("回复概率", "对每条新评论自动回复的概率，范围建议 0 到 1。", 2))
    # 提示词相关配置
    prompt: str = Field(
        default=(
            "你是'{bot_personality}'，你的好友'{nickname}'在'{created_time}'评论了你QQ空间上的一条内容为"
            "'{content}'的说说，你的好友对该说说的评论为:'{comment_content}'，"
            "现在是'{current_time}'，你想要对此评论进行回复，你对该好友的印象是:"
            "'{impression}'，若与你的印象点相关，可以适当回复相关内容，无关则忽略此印象，"
            "{bot_expression}，回复的平淡一些，简短一些，说中文，不要刻意突出自身学科背景，不要浮夸，不要夸张修辞，"
            "不要输出多余内容(包括前后缀，冒号和引号，括号()，表情包，at或 @等 )。只输出回复内容"
        ),
        description=(
            "自动回复评论的提示词，占位符包括{current_time}（当前时间），{bot_personality}（人格），{"
            "nickname}（评论者昵称），{created_time}（评论时间），{"
            "content}（说说内容），{comment_content}（评论内容），{impression}（对评论者的印象点），{"
            "bot_expression}（表达方式）"
        ),
        json_schema_extra=_ui("自动回评论提示词", "控制回复自己说说评论时生成回复内容的提示词。", 3),
    )

class ImageGenerateConfig(PluginConfigBase):
    """图片生成配置"""

    __ui_label__ = "openai格式图片生成配置"
    __ui_order__ = 6

    # AI生图相关配置
    base_url: str = Field(default="https://ark.cn-beijing.volces.com/api/v3", description="AI生图服务地址", json_schema_extra=_ui("生图服务地址", "OpenAI 兼容格式的图片生成 API 地址。", 0))
    model: str = Field(default="doubao-seedream-5-0-260128", description="AI生图使用的模型", json_schema_extra=_ui("生图模型", "用于生成 QQ 空间配图的模型名称。", 1))
    api_key: str = Field(default="your_api_key", description="AI生图服务API Key", json_schema_extra=_ui("生图 API Key", "图片生成服务的 API Key。", 2))
    enable_reference: bool = Field(default=False, description="AI生图是否启用参考图功能（需图生图模型）", json_schema_extra=_ui("启用参考图", "开启后会把参考图一起传给支持图生图的模型。", 3))
    reference: str = Field(default="", description="AI生图参考图URL或本地路径，启用参考图功能时使用", json_schema_extra=_ui("参考图", "参考图 URL 或本地路径，仅启用参考图时使用。", 4))
    prompt: str = Field(
        default=(
            "请根据以下QQ空间说说内容配图，并构建生成配图的风格和prompt。说说主人信息：'{personality}'。说说内容:'{"
            "message}'。请注意：仅回复用于生成图片的prompt，不要输出多余内容(包括前后缀，冒号和引号，括号()，表情包，at或 @等 )"
        ),
        description="AI生图提示词，占位符包括{personality}（说说主人信息），{message}（说说内容）",
        json_schema_extra=_ui("生图提示词", "根据 QQ 空间说说内容生成配图 prompt 的提示词。", 5),
    )
    ref_prompt: str = Field(
        default="说说主人的人设参考图片将随同提示词一起发送给生图AI，可使用'以参考图片风格'或'根据图中人物'等描述引导生成风格",
        description="启用参考图时的附加提示词",
        json_schema_extra=_ui("参考图附加提示词", "启用参考图时追加给生图模型的提示词。", 6),
    )
    
class AuthorityConfig(PluginConfigBase):
    """权限配置。"""

    __ui_label__ = "权限配置"
    __ui_order__ = 7

    # 发说说指令权限
    send_authority_type: str = Field(default="blacklist", description="发说说指令权限控制方式：blacklist（黑名单，禁止黑名单中的QQ号使用指令）/whitelist（白名单，仅允许白名单中的QQ号使用指令）", json_schema_extra=_ui("发说说权限模式", "blacklist=黑名单禁止；whitelist=仅白名单允许。", 0))
    send_whitelist: list[str] = Field(default=["123456","350234"], description="允许使用发说说指令的QQ号白名单", json_schema_extra=_ui("发说说白名单", "白名单模式下允许使用发说说指令的 QQ 号。", 1))
    send_blacklist: list[str] = Field(default=["123456","350234"], description="禁止使用发说说指令的QQ号黑名单", json_schema_extra=_ui("发说说黑名单", "黑名单模式下禁止使用发说说指令的 QQ 号。", 2))
    # 读说说指令权限
    read_authority_type: str = Field(default="blacklist", description="读说说指令权限控制方式：blacklist（黑名单，禁止黑名单中的QQ号使用指令）/whitelist（白名单，仅允许白名单中的QQ号使用指令）", json_schema_extra=_ui("读说说权限模式", "blacklist=黑名单禁止；whitelist=仅白名单允许。", 3))
    read_whitelist: list[str] = Field(default=["123456","350234"], description="允许使用读说说指令的QQ号白名单", json_schema_extra=_ui("读说说白名单", "白名单模式下允许使用读说说指令的 QQ 号。", 4))
    read_blacklist: list[str] = Field(default=["123456","350234"], description="禁止使用读说说指令的QQ号黑名单", json_schema_extra=_ui("读说说黑名单", "黑名单模式下禁止使用读说说指令的 QQ 号。", 5))
    # 自动读说说任务权限
    auto_read_authority_type: str = Field(default="blacklist", description="自动读说说任务权限控制方式：blacklist（黑名单，禁止黑名单中的QQ号被自动读说说）/whitelist（白名单，仅允许白名单中的QQ号被自动读说说）", json_schema_extra=_ui("自动读权限模式", "blacklist=不读取黑名单目标；whitelist=只读取白名单目标。", 6))
    auto_read_whitelist: list[str] = Field(default=[], description="自动读说说任务的QQ号白名单", json_schema_extra=_ui("自动读白名单", "白名单模式下允许被自动读取空间的 QQ 号。", 7))
    auto_read_blacklist: list[str] = Field(default=["123456","350234"], description="自动读说说任务的QQ号黑名单", json_schema_extra=_ui("自动读黑名单", "黑名单模式下禁止被自动读取空间的 QQ 号。", 8))


class MaizonePluginConfig(PluginConfigBase):
    """插件总配置。"""
    plugin: PluginSectionConfig = Field(default_factory=PluginSectionConfig, description="插件基础配置", json_schema_extra=_ui("基础配置", "插件开关、模型与 Cookie 获取方式。", 0))
    send: SendConfig = Field(default_factory=SendConfig, description="指令发说说配置", json_schema_extra=_ui("发说说", "主动发送 QQ 空间说说相关设置。", 1))
    read: ReadConfig = Field(default_factory=ReadConfig, description="指令读说说配置", json_schema_extra=_ui("读说说", "读取和评论 QQ 空间动态相关设置。", 2))
    auto_send: AutoSendConfig = Field(default_factory=AutoSendConfig, description="自动发说说配置", json_schema_extra=_ui("自动发说说", "定时自动发送 QQ 空间说说相关设置。", 3))
    auto_read: AutoReadConfig = Field(default_factory=AutoReadConfig, description="自动读说说配置", json_schema_extra=_ui("自动读说说", "定时自动读取 QQ 空间动态相关设置。", 4))
    auto_reply: AutoReplyConfig = Field(default_factory=AutoReplyConfig, description="自动回评论配置", json_schema_extra=_ui("自动回评论", "自动回复自己说说评论相关设置。", 5))
    image: ImageGenerateConfig = Field(default_factory=ImageGenerateConfig, description="AI生图配置", json_schema_extra=_ui("AI 生图", "QQ 空间说说配图生成相关设置。", 6))
    authority: AuthorityConfig = Field(default_factory=AuthorityConfig, description="权限配置", json_schema_extra=_ui("权限配置", "命令和自动任务的 QQ 号权限控制。", 7))
