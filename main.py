from fasthtml.common import *
import matplotlib.pyplot as plt

app, rt = fast_app(hdrs=[HighlightJS()])


@rt("/convert")
def post(html: str):
    plt.figure()
    try:
        exec(html)
    except Exception as e:
        import traceback

        o = f"ERROR: {traceback.format_exc()}"
        return Titled("Error", P(o, style="font-family: monospace"))
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format="jpg")
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    return Img(src=f"data:image/jpg;base64, {my_base64_jpgData}")


@rt("/")
def get():
    txt = (
        Textarea(
            id="html",
            placeholder="plt.plot([2,3,4], [1,2,3])",
            rows=10,
            cols=10,
            # hx_post="/convert",
            # target_id="ft",
            # hx_trigger="keyup delay:1500ms",
        ),
    )

    btn = Form(
        Group(
            txt,
            Button("Plot", target_id="ft", hx_post="/convert"),
        )
    )

    return Titled(
        "Live Matplotlib",
        btn,
        Div(id="ft"),
        style="margin: 20px",
    )


serve(reload=True)
#
