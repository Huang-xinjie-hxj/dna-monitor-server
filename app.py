import datetime
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import os
import json
app = Flask(__name__)

# ─── 数据存储 ───


JSON_FILE = 'commissions_data.json'


def load_commissions():
    """从本地硬盘读取历史委托，如果文件不存在则初始化默认数据"""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取数据失败，转为初始化默认值: {e}")

    # 默认初始数据
    return [
        {"name": "你们有什么没有完成的梦想？", "content": "有什么梦想，就在这里提出来！", "date": "2026-06-04"}
    ]


def save_commissions():
    """将当前委托列表死死写入硬盘 JSON 文件，确保重启不丢失"""
    try:
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(commissions, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"持久化保存失败: {e}")


# 在程序启动时，自动从硬盘加载历史数据
commissions = load_commissions()
# ─── 统一的前端布局生成函数 ───
def render_page(active_tab, body_content):
    """
    通过这个函数动态生成带有侧边栏的完整页面，避免了 Jinja2 找不到 base 模板的问题
    """
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>黄辛杰 (Huang Xin jie) - 个人主页</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8f9fa; font-family: system-ui, -apple-system, sans-serif; }}
            .sidebar {{ width: 260px; position: fixed; top: 0; bottom: 0; left: 0; background-color: #1e293b; color: #fff; padding: 20px; z-index: 100; }}
            .main-content {{ margin-left: 260px; padding: 40px; }}
            .profile-img {{ width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid #3b82f6; margin-bottom: 10px; }}
            .nav-link {{ color: #cbd5e1; margin-bottom: 8px; border-radius: 6px; padding: 10px 15px; text-decoration: none; display: block; }}
            .nav-link:hover, .nav-link.active {{ background-color: #334155; color: #fff; }}
            .service-card {{ border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.2s; background: white; padding: 24px; text-align: center; }}
            .service-card:hover {{ transform: translateY(-5px); }}
            .pdf-container {{ height: 85vh; width: 100%; border-radius: 12px; border: 1px solid #e2e8f0; }}
            .back-btn {{ margin-bottom: 20px; display: inline-block; }}
        </style>
    </head>
    <body>

        <div class="sidebar">
            <div class="text-center mb-4">
                <img src="/static/avatar.jpg" onerror="this.src='https://via.placeholder.com/150'" class="profile-img" alt="头像">
                <h5 class="mt-2 mb-0" style="color: #f8fafc;">黄辛杰</h5>
                <small style="color: #94a3b8;">Huang Xin jie</small>
            </div>
            <hr style="border-color: #334155;">
            <nav class="nav flex-column">
                <a class="nav-link {"active" if active_tab == "cv" else ""}" href="/"><i class="bi bi-file-earmark-person me-2"></i> 简历 (CV)</a>
                <a class="nav-link {"active" if active_tab == "news" else ""}" href="/news"><i class="bi bi-newspaper me-2"></i> 新闻 (News)</a>
                <a class="nav-link {"active" if active_tab == "service" else ""}" href="/service"><i class="bi bi-briefcase me-2"></i> 服务 (Service)</a>
                <a class="nav-link {"active" if active_tab == "link" else ""}" href="/link"><i class="bi bi-link-45deg me-2"></i> 链接 (Link)</a>
                <a class="nav-link {"active" if active_tab == "commission" else ""}" href="/commission"><i class="bi bi-clipboard-check me-2"></i> 委托 (Commission)</a>
            </nav>
        </div>

        <div class="main-content">
            {body_content}
        </div>

    </body>
    </html>
    """
    return render_template_string(html_template)


# ─── 1. 简历部分 (CV) ───
@app.route('/')
def cv():
    body = """
    <h3 class="mb-4">📄 个人简历 / Curriculum Vitae</h3>
    <object class="pdf-container" data="/static/cv.pdf" type="application/pdf">
        <p>您的浏览器不支持直接预览 PDF，请点击这里 <a href="/static/cv.pdf">下载 PDF 查看</a>。</p>
    </object>
    """
    return render_page('cv', body)


# ─── 2. 新闻部分 (News 主页) ───
@app.route('/news')
def news():
    body = """
    <h3 class="mb-4">📰 最新动态 / News</h3>

    <div class="list-group shadow-sm mb-5">
        <a href="/news/dna-optimization" class="list-group-item list-group-item-action p-3">
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">💡 成功找到三国杀OL比赛服的出将规律</h5>
                <small class="text-muted">2026-05-26</small>
            </div>
            <p class="mb-1 text-muted">青春没有售价，冠军就在眼下!</p>
        </a>
        <a href="/news/proposal-passed" class="list-group-item list-group-item-action p-3">
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">黄辛杰的网站第一次开张</h5>
                <small class="text-muted">2026-06-05</small>
            </div>
            <p class="mb-1 text-muted">It's my birthday.</p>
        </a>
    </div>

    <div class="card p-4 shadow-sm" style="max-width: 500px; background: #f1f5f9; border: none; border-radius: 12px;">
        <h5>📩 订阅动态更新</h5>
        <p class="text-muted small">在新闻更新的时候，会向你的邮箱发送消息。</p>
        <form action="/subscribe" method="POST" class="d-flex gap-2">
            <input type="email" name="email" class="form-control" placeholder="your-email@academic.com" required>
            <button type="submit" class="btn btn-primary px-4">订阅</button>
        </form>
    </div>
    """
    return render_page('news', body)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        subscribed_emails.append(email)
        print(f"📬 [本地电脑日志通知] 收到新用户订阅邮箱: {email}")
    return redirect(url_for('news'))


# ─── 2.1 新闻子网站 1 ───
@app.route('/news/dna-optimization')
def news_detail_1():
    body = """
    <a href="/news" class="btn btn-sm btn-outline-secondary back-btn"><i class="bi bi-arrow-left"></i> 返回新闻列表</a>
    <div class="card p-5 shadow-sm border-0" style="border-radius: 16px; background: white;">
        <h2 class="text-dark mb-2">成功找到三国杀OL比赛服的出将规律</h2>
        <p class="text-muted small">发布时间: 2026-05-26 | 作者: 黄辛杰</p>
        <hr>
        <p class="lead" style="line-height: 1.8;">
            还在为比赛选不到强大的武将而迷茫吗？还在为斗地主不知道如何叫分而感到心累吗？我知晓着你更有可能是什么武将，而你几乎一无所知。
            重磅推荐——黄辛杰最新的研究成果，针对OL斗地主的发将规律的彻底研究，彻底扫清你在赛场上的所以阻碍。
            只要2豆(100RMB)，整个赛季持续服务，给出最可信的结论，让你知道你想知道的一切，一人购买，整俱乐部可用。请尊重知识与劳动，购买后不要传给其他俱乐部的同学。
            青春没有售价，冠军就在眼下
        </p>
        <h4 class="mt-4 text-primary">获取方式</h4>
        <p style="line-height: 1.7; color: #475569;">
            详情请看服务（service）界面
        </p>
    </div>
    """
    return render_page('news', body)


# ─── 2.2 新闻子网站 2 ───
@app.route('/news/proposal-passed')
def news_detail_2():
    body = """
    <a href="/news" class="btn btn-sm btn-outline-secondary back-btn"><i class="bi bi-arrow-left"></i> 返回新闻列表</a>
    <div class="card p-5 shadow-sm border-0" style="border-radius: 16px; background: white;">
        <h2 class="text-dark mb-2">黄辛杰的网站第一次开张</h2>
        <p class="text-muted small">发布时间: 2026-06-05 | 作者: 黄辛杰</p>
        <hr>
        <p class="lead" style="line-height: 1.8;">
            2026年6月5日凌晨，黄辛杰突发奇想，创建了这个网站。这是非常有历史意义的一刻。
        </p>
        <h4 class="mt-4 text-success">意见反馈与联系</h4>
        <p style="line-height: 1.7; color: #475569;">
            如有任何建议，请发送邮件联系。
            hxj15921278031@mail.ustc.edu.cn
        </p>
    </div>
    """
    return render_page('news', body)


# ─── 3. 服务部分 (Service 主页) ───
@app.route('/service')
def service():
    body = """
    <h3 class="mb-4">服务 / Services</h3>
    <div class="row g-4">
        <div class="col-md-4">
            <div class="service-card">
                <div class="fs-1 text-primary mb-3"><i class="bi bi-code-slash"></i></div>
                <h5>三国杀OL斗地主出将秘籍</h5>
                <p class="text-muted small" style="min-height: 72px;">青春没有售价，冠军就在眼下！</p>
                <a href="/service/brownian-dynamics" class="btn btn-sm btn-outline-primary mt-2">Learn More</a>
            </div>
        </div>
        <div class="col-md-4">
            <div class="service-card">
                <div class="fs-1 text-success mb-3"><i class="bi bi-file-earmark-bar-graph"></i></div>
                <h5>python代码代写</h5>
                <p class="text-muted small" style="min-height: 72px;">特别擅长帮大学生完成作业与科研。黄辛杰写的，说出去都倍有面儿。</p>
                <a href="/service/data-pipeline" class="btn btn-sm btn-outline-success mt-2">Learn More</a>
            </div>
        </div>
        <div class="col-md-4">
            <div class="service-card">
                <div class="fs-1 text-warning mb-3"><i class="bi bi-lightbulb"></i></div>
                <h5>物理竞赛家教指导</h5>
                <p class="text-muted small" style="min-height: 72px;">39届全国中学生物理竞赛上海赛区省一等奖，绰绰有余考入中科大少年班，十余名学生辅导经验，值得信赖。</p>
                <a href="/service/physics-consulting" class="btn btn-sm btn-outline-warning mt-2">Learn More</a>
            </div>
        </div>
        <div class="col-md-4">
            <div class="service-card">
                <div class="fs-1 text-warning mb-3"><i class="bi bi-lightbulb"></i></div>
                <h5>游戏陪玩</h5>
                <p class="text-muted small" style="min-height: 72px;">王者荣耀：边路雅典娜，优先断兵线，是包赢滴。三国杀：还得是全世界最好玩的游戏。</p>
                <a href="/service/peiwan" class="btn btn-sm btn-outline-warning mt-2">Learn More</a>
            </div>
        </div>
    </div>
    """
    return render_page('service', body)


# ─── 3.1 服务子网站 1 ───
@app.route('/service/brownian-dynamics')
def service_detail_1():
    body = """
    <a href="/service" class="btn btn-sm btn-outline-secondary back-btn"><i class="bi bi-arrow-left"></i> 返回服务主页</a>
    <div class="card p-5 shadow-sm border-0" style="border-radius: 16px; background: white;">
        <h3 class="text-warning mb-3"><i class="bi bi-lightbulb me-2"></i> 三国杀OL斗地主秘籍</h3>
        <p style="line-height: 1.8;">
            还在为比赛选不到强大的武将而迷茫吗？还在为斗地主不知道如何叫分而感到心累吗？我知晓着你更有可能是什么武将，而你几乎一无所知。
            重磅推荐——黄辛杰最新的研究成果，针对OL斗地主的发将规律的彻底研究，彻底扫清你在赛场上的所以阻碍。
            只要2豆(100RMB)，整个赛季持续服务，给出最可信的结论，让你知道你想知道的一切，一人购买，整俱乐部可用。请尊重知识与劳动，购买后不要传给其他俱乐部的同学。
            青春没有售价，冠军就在眼下！
        </p>
        <p style="line-height: 1.7; color: #475569;">
            100RMB/赛季。一百块钱交个朋友，包你这赛季一骑绝尘。（不退款，不对赌，不打折）有需求请联系邮箱:hxj15921278031@mail.ustc.edu.cn。
        </p>
        <hr class="my-4">
        <div class="text-center" style="max-width: 250px; background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px dashed #cbd5e1;">
            <h6 class="text-muted mb-2"><i class="bi bi-credit-card-2-front me-1"></i> 收款码</h6>
            <img src="/static/pay_code.jpg" onerror="this.src='https://via.placeholder.com/200?text=Pay+Code'" class="img-fluid rounded mb-2" style="max-height: 200px; object-fit: contain;" alt="收款码">
            <small class="text-muted d-block">扫码支付请备注需求名称与联系方式</small>
        </div>
    </div>
    </div>
    """
    return render_page('service', body)


# ─── 3.2 服务子网站 2 ───
@app.route('/service/data-pipeline')
def service_detail_2():
    body = """
    <a href="/service" class="btn btn-sm btn-outline-secondary back-btn"><i class="bi bi-arrow-left"></i> 返回服务主页</a>
    <div class="card p-5 shadow-sm border-0" style="border-radius: 16px; background: white;">
        <h3 class="text-success mb-3"><i class="bi bi-file-earmark-bar-graph me-2"></i> python代写</h3>
        <p style="line-height: 1.8;">
            大学的大作业？棘手的科研任务？都可以交给我。
        </p>
        <p style="line-height: 1.7; color: #475569;">
            价格面议。有需求请联系邮箱:hxj15921278031@mail.ustc.edu.cn。
        </p>
        <hr class="my-4">
        <div class="text-center" style="max-width: 250px; background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px dashed #cbd5e1;">
            <h6 class="text-muted mb-2"><i class="bi bi-credit-card-2-front me-1"></i> 收款码</h6>
            <img src="/static/pay_code.jpg" onerror="this.src='https://via.placeholder.com/200?text=Pay+Code'" class="img-fluid rounded mb-2" style="max-height: 200px; object-fit: contain;" alt="收款码">
            <small class="text-muted d-block">扫码支付请备注需求名称与联系方式</small>
        </div>
    </div>
    """
    return render_page('service', body)


# ─── 3.3 服务子网站 3 ───
@app.route('/service/physics-consulting')
def service_detail_3():
    body = """
    <a href="/service" class="btn btn-sm btn-outline-secondary back-btn"><i class="bi bi-arrow-left"></i> 返回服务主页</a>
    <div class="card p-5 shadow-sm border-0" style="border-radius: 16px; background: white;">
        <h3 class="text-warning mb-3"><i class="bi bi-lightbulb me-2"></i> 高中物理竞赛家教</h3>
        <p style="line-height: 1.8;">
            39届全国中学生物理竞赛上海赛区省一等奖，绰绰有余考入中科大少年班，十余名学生辅导经验，值得信赖。
        </p>
        <p style="line-height: 1.7; color: #475569;">
            约270RMB/h，按照年级不同与学生基础不同略有浮动。有需求请联系邮箱:hxj15921278031@mail.ustc.edu.cn。
        </p>
        <hr class="my-4">
        <div class="text-center" style="max-width: 250px; background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px dashed #cbd5e1;">
            <h6 class="text-muted mb-2"><i class="bi bi-credit-card-2-front me-1"></i> 收款码</h6>
            <img src="/static/pay_code.jpg" onerror="this.src='https://via.placeholder.com/200?text=Pay+Code'" class="img-fluid rounded mb-2" style="max-height: 200px; object-fit: contain;" alt="收款码">
            <small class="text-muted d-block">扫码支付请备注需求名称与联系方式</small>
        </div>
    </div>
    """
    return render_page('service', body)
@app.route('/service/peiwan')
def service_detail_4():
    body = """
    <a href="/service" class="btn btn-sm btn-outline-secondary back-btn"><i class="bi bi-arrow-left"></i> 返回服务主页</a>
    <div class="card p-5 shadow-sm border-0" style="border-radius: 16px; background: white;">
        <h3 class="text-warning mb-3"><i class="bi bi-lightbulb me-2"></i> 游戏陪玩</h3>
        <p style="line-height: 1.8;">
            提供情绪价值，和我玩一把，保证产生强烈的情绪。有需求请联系邮箱:hxj15921278031@mail.ustc.edu.cn。
        </p>
        <p style="line-height: 1.7; color: #475569;">
            10RMB/h，象征意义的友情价。没有技术，全是有趣的灵魂。
        </p>
        <hr class="my-4">
        <div class="text-center" style="max-width: 250px; background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px dashed #cbd5e1;">
            <h6 class="text-muted mb-2"><i class="bi bi-credit-card-2-front me-1"></i> 收款码</h6>
            <img src="/static/pay_code.jpg" onerror="this.src='https://via.placeholder.com/200?text=Pay+Code'" class="img-fluid rounded mb-2" style="max-height: 200px; object-fit: contain;" alt="收款码">
            <small class="text-muted d-block">扫码支付请备注需求名称与联系方式</small>
        </div>
    </div>
    """
    return render_page('service', body)

# ─── 4. 链接部分 (Links) ───
@app.route('/link')
def link():
    body = """
    <h3 class="mb-4">🔗 社交与学术平台 / Links</h3>
    <div class="row g-3" style="max-width: 600px;">

        <div class="col-6">
            <a href="https://space.bilibili.com/352867192?spm_id_from=333.337.0.0" target="_blank" class="btn w-100 p-3 text-start text-white" style="background-color: #fb7299; border: none; border-radius: 10px;">
                <i class="bi bi-play-circle-fill me-2"></i> 哔哩哔哩 / Bilibili
            </a>
        </div>

        <div class="col-6">
            <a href="https://www.goofish.com/personal?spm=a21ybx.search.nav.1.37db1d0aHkWzlj" target="_blank" class="btn w-100 p-3 text-start text-dark" style="background-color: #ffda00; border: none; border-radius: 10px; font-weight: 500;">
                <i class="bi bi-bag-dash-fill me-2"></i> 闲鱼 / XianYu
            </a>
        </div>

        <div class="col-6">
            <a href="https://www.douyin.com/user/MS4wLjABAAAA-w7yLU--n5lEQJGgBnmB3M_h1LjHyni5MrMxjaLImDNV2hSl2ijOUIY_B8AikdJK?from_tab_name=main" target="_blank" class="btn w-100 p-3 text-start text-white" style="background-color: #161823; border: none; border-radius: 10px;">
                <i class="bi bi-tiktok me-2"></i> 抖音 / Douyin
            </a>
        </div>

        <div class="col-6">
            <a href="mailto:hxj15921278031@mail.ustc.edu.cn" class="btn w-100 p-3 text-start text-white" style="background-color: #64748b; border: none; border-radius: 10px;">
                <i class="bi bi-envelope-fill me-2"></i> 电子邮件 / Email:hxj15921278031@mail.ustc.edu.cn
            </a>
        </div>

    </div>
    """
    return render_page('link', body)


# ─── 5. 委托部分 (Commission - 支持重启留存与在线删除) ───
@app.route('/commission', methods=['GET', 'POST'])
def commission():
    if request.method == 'POST':
        user_name = request.form.get('username', '匿名用户')
        content_text = request.form.get('content', '')
        if content_text:
            # 1. 动态追加新数据
            commissions.append({
                "name": user_name,
                "content": content_text,
                "date": datetime.date.today().strftime("%Y-%m-%d")
            })
            # 2. 🚀 核心修改：立刻同步写入硬盘文件，防备程序随时重启
            save_commissions()

        return redirect(url_for('commission'))

    # 在 Python 内部动态渲染委托列表
    cards_html = ""
    # 使用 enumerate 获得每一条委托的独立索引(idx)，方便精准删除
    for idx, c in enumerate(commissions):
        cards_html = f"""
        <div class="p-3 border rounded shadow-sm" style="background-color: #fdfdfd; border-left: 5px solid #198754 !important; margin-bottom: 15px;">
            <div class="d-flex justify-content-between align-items-center mb-1">
                <div>
                    <strong class="text-dark">{c['name']}</strong>
                    <small class="text-muted ms-2">{c['date']}</small>
                </div>
                <form action="/delete_commission/{idx}" method="POST" style="margin: 0;">
                    <button type="submit" class="btn btn-sm btn-link text-danger p-0 text-decoration-none" onclick="return confirm('确定要删除这条委托吗？')">
                        <i class="bi bi-trash3"></i> 删除
                    </button>
                </form>
            </div>
            <p class="mb-0 text-secondary" style="font-size: 14px; white-space: pre-wrap;">{c['content']}</p>
        </div>
        """ + cards_html  # 最新提交的委托显示在公示板最上方

    body = f"""
    <h3 class="mb-4">💼 需求委托与协作 / Commission</h3>
    <div class="row g-4">
        <div class="col-md-5">
            <div class="card p-4 shadow-sm border-0" style="border-radius: 12px;">
                <h5>提交新委托</h5>
                <hr>
                <form action="/commission" method="POST">
                    <div class="mb-3">
                        <label class="form-label small text-muted">您的姓名/机构</label>
                        <input type="text" name="username" class="form-control" placeholder="合作者名称" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label small text-muted">委托内容需求</label>
                        <textarea name="content" class="form-control" rows="5" placeholder="请详述您的合作或需求..." required></textarea>
                    </div>
                    <button type="submit" class="btn btn-success w-100">发布并挂牌公示</button>
                </form>
            </div>
        </div>

        <div class="col-md-7">
            <div class="card p-4 shadow-sm border-0" style="max-height: 80vh; overflow-y: auto; border-radius: 12px;">
                <h5 class="text-success"><i class="bi bi-pin-angle-fill me-2"></i> 委托项目挂牌公示看板</h5>
                <hr>
                <div class="d-flex flex-column">
                    {cards_html}
                </div>
            </div>
        </div>
    </div>
    """
    return render_page('commission', body)


# ─── 处理删除动作的后台接口 ───
@app.route('/delete_commission/<int:idx>', methods=['POST'])
def delete_commission(idx):
    try:
        if 0 <= idx < len(commissions):
            # 1. 从内存列表中剃除
            commissions.pop(idx)
            # 2. 🚀 核心修改：立刻将剃除后的新列表重新覆写到硬盘文件
            save_commissions()
    except Exception as e:
        print(f"删除失败: {e}")
    return redirect(url_for('commission'))

# 统一的数据导出 API
@app.route('/api/export_data', methods=['GET'])
def export_data():
    return jsonify({
        "emails": subscribed_emails,
        "commissions": commissions
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)