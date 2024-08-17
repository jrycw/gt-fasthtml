import polars as pl
from fasthtml.common import NotStr, Title, Titled, fast_app
from great_tables import GT, html
from great_tables.data import sza

app, rt = fast_app()


@rt("/")
def get():
    """
    https://docs.fastht.ml/tutorials/quickstart_for_web_devs.html#strings-and-conversion-order
    """
    sza_pivot = (
        pl.from_pandas(sza)
        .filter((pl.col("latitude") == "20") & (pl.col("tst") <= "1200"))
        .select(pl.col("*").exclude("latitude"))
        .drop_nulls()
        .pivot(values="sza", index="month", on="tst", sort_columns=True)
    )

    sza_tbl = (
        GT(sza_pivot, rowname_col="month")
        .data_color(
            domain=[90, 0],
            palette=["rebeccapurple", "white", "orange"],
            na_color="white",
        )
        .tab_header(
            title="Solar Zenith Angles from 05:30 to 12:00",
            subtitle=html("Average monthly values at latitude of 20&deg;N."),
        )
        .sub_missing(missing_text="")
    )

    return (
        Title("FastHTML-GT Website"),
        Titled("Great Tables shown in FastHTML", style="text-align:center"),
        NotStr(sza_tbl.as_raw_html()),
    )
