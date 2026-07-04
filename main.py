import urllib.error
import urllib.parse
import urllib.request

from flask import Flask, Response, jsonify, redirect, render_template, request, send_from_directory, stream_with_context, url_for

from backend import products_categories, products_list

app = Flask(__name__)
REMOTE_IMAGE_BASES = [
    "https://omo-oss-image1.thefastimg.com/portal-saas/pg2024053117235883285/cms/image/",
    "https://omo-oss-image.thefastimg.com/portal-saas/pg2024053117235883285/cms/image/",
]
REMOTE_IMAGE_REFERERS = [
    "https://thepacifichomes.us/",
    "https://en.hbjrx.com/",
]


def build_product_image_url(filename):
    return url_for("product_image", filename=filename)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/products/<int:no>')
def products(no):
        no = "26" if str(no) == "24" else str(no)
        category = products_categories.get(no)
        if not category or "products" not in category:
                return "Category not found", 404

        imgs = [products_list[prod_no]["images"][0] for prod_no in category["products"]]
        titles = [products_list[prod_no]["name"] for prod_no in category["products"]]
        desc = [products_list[prod_no]["desc"] for prod_no in category["products"]]
        data = [
                category["name"],
                category["products"],
                imgs,
                titles,
                desc,
                len(titles),
        ]
        return render_template("catalog.html", data=data)


@app.route('/product_details/<int:no>')
def product_details(no):
        no = str(no)
        if no not in products_list:
                return "Product not found", 404
        magnifier_line = "[{"
        for img in products_list[str(no)]["images"]:
            magnifier_line += f"url:{build_product_image_url(img)},name:{products_list[str(no)]['name']}"
            magnifier_line += "},{"
        magnifier_line += "]"
        data = [products_list[str(no)]["images"],
                products_list[str(no)]["name"],
                magnifier_line,
                products_list[str(no)]["desc"],
                products_list[no]["detail"]]
        return render_template(f"product_detailed.html", data=data)

@app.route('/news/<int:no>')
def news(no):
        return render_template(f"news_list/{str(no)}.html")
@app.route('/news_details/<int:no>')
def news_details(no):
        return render_template(f"news_details/{str(no)}.html")




@app.route('/company')
def company():
    return render_template("company.html")

@app.route('/qualification/<int:no>')
def qualification(no):
    return render_template(f"qualification/{str(no)}.html")

@app.route('/culture')
def culture():
    return render_template("culture.html")
@app.route('/project')
def project():
    return render_template("project.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/taglist')
def taglist():
    return render_template("taglist1b1a.html")

@app.route('/success')
def success():
    return render_template("successfully1b1a.html")

@app.route('/search')
def search():
    return render_template("search8213.html")


@app.route('/product-image/<path:filename>')
def product_image(filename):
    quoted_filename = urllib.parse.quote(filename)
    last_error = None

    for base_url in REMOTE_IMAGE_BASES:
        image_url = f"{base_url}{quoted_filename}"
        for referer in REMOTE_IMAGE_REFERERS:
            remote_request = urllib.request.Request(
                image_url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Referer": referer,
                    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                },
            )

            try:
                remote_response = urllib.request.urlopen(remote_request, timeout=30)
                content_type = remote_response.headers.get("Content-Type", "application/octet-stream")
                cache_control = remote_response.headers.get("Cache-Control", "public, max-age=86400")
                content_length = remote_response.headers.get("Content-Length")
                break
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
                last_error = exc
        else:
            continue
        break
    else:
        error_code = getattr(last_error, "code", "unavailable")
        return f"Image unavailable: {error_code}", 502

    def generate():
        try:
            while True:
                chunk = remote_response.read(64 * 1024)
                if not chunk:
                    break
                yield chunk
        finally:
            remote_response.close()

    response = Response(stream_with_context(generate()), mimetype=content_type)
    response.headers["Cache-Control"] = cache_control
    if content_length:
        response.headers["Content-Length"] = content_length
    return response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico")


@app.route('/css/<path:filename>')
def legacy_css(filename):
    return send_from_directory(f"{app.static_folder}/css", filename)


@app.route('/npublic/<path:filename>')
def legacy_npublic(filename):
    return send_from_directory(f"{app.static_folder}/npublic", filename)


@app.route('/upload/<path:filename>')
def legacy_upload(filename):
    return send_from_directory(f"{app.static_folder}/upload", filename)


@app.route('/www.googletagmanager.com/<path:filename>')
def legacy_gtm(filename):
    query = f"?{request.query_string.decode()}" if request.query_string else ""
    target = f"https://www.googletagmanager.com/{filename}{query}"
    if filename.startswith("gtm"):
        target = f"https://www.googletagmanager.com/gtm.js{query}"
    return redirect(target, code=302)


@app.route('/omo-oss-image.thefastimg.com/<path:filename>')
def legacy_thefastimg(filename):
    return redirect(f"https://omo-oss-image.thefastimg.com/{filename}", code=302)


@app.route('/omo-oss-image1.thefastimg.com/<path:filename>')
def legacy_thefastimg_alt(filename):
    return redirect(f"https://omo-oss-image1.thefastimg.com/{filename}", code=302)


@app.route('/m2cdn.fastindexs.com/<path:filename>')
def legacy_fastindexs(filename):
    return redirect(f"https://m2cdn.fastindexs.com/{filename}", code=302)


@app.route('/dcloud-static01.faststatics.com/<path:filename>')
def legacy_faststatics(filename):
    return redirect(f"https://dcloud-static01.faststatics.com/{filename}", code=302)


@app.route('/portal-saas/<path:filename>')
@app.route('/product_details/portal-saas/<path:filename>')
def legacy_portal_saas_image(filename):
    return redirect(
        f"https://omo-oss-image.thefastimg.com/portal-saas/{filename}",
        code=302,
    )


@app.route('/ndesigner/api/gray', methods=['POST'])
def legacy_gray():
    return jsonify({"code": 204})


@app.route('/fwebapi/cms/baseConfig/get')
def legacy_base_config():
    return jsonify({"code": 200, "data": {}})


@app.route('/icp')
def legacy_icp():
    return redirect("https://beian.miit.gov.cn/", code=302)


@app.route('/index.html')
def legacy_index():
    return main()


@app.route('/company.html')
def legacy_company():
    return company()


@app.route('/culture.html')
def legacy_culture():
    return culture()


@app.route('/project.html')
def legacy_project():
    return project()


@app.route('/contact.html')
def legacy_contact():
    return contact()


@app.route('/taglist1b1a.html')
def legacy_taglist():
    return taglist()


@app.route('/successfully1b1a.html')
@app.route('/successfully.html')
def legacy_success():
    return success()


@app.route('/search8213.html')
def legacy_search():
    return search()


@app.route('/news_list/<path:filename>')
def legacy_news_list_template(filename):
    return render_template(f"news_list/{filename}")


@app.route('/news_details/<path:filename>')
def legacy_news_details_template(filename):
    return render_template(f"news_details/{filename}")


@app.route('/news_Detail_1/<path:filename>')
def legacy_news_detail_alt_template(filename):
    return render_template(f"news_Detail_1/{filename}")


@app.route('/project/<path:filename>')
def legacy_project_template(filename):
    return render_template(f"project/{filename}")


@app.route('/qualification/<path:filename>')
def legacy_qualification_template(filename):
    return render_template(f"qualification/{filename}")


@app.route('/products_details/<path:filename>')
def legacy_product_details_template(filename):
    return render_template(f"products_details/{filename}")


@app.route('/successfully/<path:filename>')
def legacy_successfully_template(filename):
    return render_template(f"successfully/{filename}")

if __name__ == '__main__':
    app.run()
