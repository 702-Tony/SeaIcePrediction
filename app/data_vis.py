import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
# def get_violin_plots():
#     df_1980 = DF_DATASET[DF_DATASET['year'].isin([1980,1985,1990,1995,2000, 2005, 2010, 2015])]
#
#     ax_n = sns.violinplot(x='year', y='n_extent', data=df_1980, split=True)
#
#
#     pngImage = io.BytesIO()
#     ax_fig = ax_n.save_fig(pngImage)
#     # FigureCanvas(ax_n).print_png(pngImage)
#     # Encode PNG image to base64 string
#     pngImageB64String = "data:image/png;base64,"
#     pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
#     return pngImageB64String
