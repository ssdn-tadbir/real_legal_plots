import numpy as np
from matplotlib import pyplot as plt, gridspec
from pathlib import Path
import imageio as iio
import arabic_reshaper
from persiantools import digits
from bidi.algorithm import get_display
import pandas as pd

plt.rcParams["figure.figsize"] = (11, 12)


def cast_to_int(value):
    return int(round(value))


rows = {
    1: type('Dimension', (), {"height": 0.1, 'width': [0.2, 0.4]}),
    2: type('Dimension', (), {"height": 0.2, 'width': []}),
    3: type('Dimension', (), {"height": 0.25, 'width': [0.15, 0.3]}),
    4: type('Dimension', (), {"height": 0.70, 'width': []}),
    5: type('Dimension', (), {"height": 0.75, 'width': [0.15, 0.3]}),
    6: type('Dimension', (), {"height": 1, 'width': []}),
}

dat = [1, 2, 3, 4, 5, 6, 7, 8, -9, 8, 7, 6, 5, 4, 9]


def remove_axis(ax0):
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['left'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.set_xticks([])
    ax0.set_yticks([])
    ax0.set_anchor('W')
    return ax0


fonts = type("Fonts", (), {
    'yekan_bold': Path("utils/fonts/fonts/IRANYEKANBOLD.TTF"),
    'yekan_extra_bold': Path("utils/fonts/fonts/IRANYEKANEXTRABOLD.TTF"),
    'yekan_light': Path("utils/fonts/fonts/IRANYEKANLIGHT.TTF"),
    'yekan': Path("utils/fonts/fonts/IRANYEKANBLACK.TTF"),
    'yekan_num': Path("utils/fonts/fonts/IRANYEKANREGULARFANUM.TTF"),

})


class Plot:

    def __init__(self, width=100, height=100):
        self.gs = None
        self.width = width
        self.height = height
        self.logo_dailytahlil = iio.imread("utils/img/logo_daily_tahlil.png")
        self.logo_tadbirgaran = iio.imread("utils/img/logo_kargozari.png")
        self.icon_bars = iio.imread("utils/img/icon_bars.png")

    def grid_method(self):
        self.gs = gridspec.GridSpec(self.height, self.width, wspace=0, hspace=0)
        ax_daily_tahlil_logo = plt.subplot(
            self.gs[:cast_to_int(rows[1].height * self.height), :cast_to_int(rows[1].width[0] * self.width)])

        ax_tadbirgaran_logo = plt.subplot(
            self.gs[:cast_to_int(rows[1].height * self.height),
            cast_to_int((rows[1].width[0] + 0.02) * self.width):cast_to_int(rows[1].width[1] * self.width)])

        ax_main_title = plt.subplot(
            self.gs[:cast_to_int(rows[1].height * self.height), cast_to_int(rows[1].width[1] * self.width):])

        ax_legend_first_1 = plt.subplot(
            self.gs[cast_to_int(rows[2].height * self.height):cast_to_int(rows[3].height * self.height),
            :cast_to_int(rows[3].width[0] * self.width)])

        ax_legend_first_2 = plt.subplot(
            self.gs[cast_to_int(rows[2].height * self.height):cast_to_int(rows[3].height * self.height),
            cast_to_int(rows[3].width[0] * self.width):cast_to_int(rows[3].width[1] * self.width)])

        ax_legend_first_3 = plt.subplot(
            self.gs[cast_to_int(rows[2].height * self.height):cast_to_int(rows[3].height * self.height),
            cast_to_int(rows[3].width[1] * self.width):])

        ax_others = plt.subplot(self.gs[cast_to_int(rows[3].height * self.height):, :])

        ax_daily_tahlil_logo = remove_axis(ax_daily_tahlil_logo)
        ax_tadbirgaran_logo = remove_axis(ax_tadbirgaran_logo)
        ax_main_title = remove_axis(ax_main_title)
        ax_legend_first_1 = remove_axis(ax_legend_first_1)
        ax_legend_first_2 = remove_axis(ax_legend_first_2)
        ax_legend_first_3 = remove_axis(ax_legend_first_3)

        ax_daily_tahlil_logo.imshow(self.logo_tadbirgaran)
        # title = "این یک متن تست است." + "(ُ1401/10/07)"
        # title = digits.en_to_fa(title)
        # title = get_display(arabic_reshaper.reshape(title))

        # title = "خروج پول حقیقی"
        # title = digits.en_to_fa(title)
        # title = get_display(arabic_reshaper.reshape(title))

        # ax_legend_first_1.bar([0, 1], [0, 1])
        # ax_legend_first_1.text(5, -20, title, font=fonts.yekan_light, size=14, color="gray")
        # ax_legend_first_1.imshow(self.icon_bars, )
        # ax_legend_first_2.imshow(self.icon_bars, )
        # ax_legend_first_3.imshow(self.icon_bars, )
        ax_tadbirgaran_logo.imshow(self.logo_dailytahlil)
        title = "این یک متن تست است." + "(ُ1401/10/07)"
        title = digits.en_to_fa(title)
        title = get_display(arabic_reshaper.reshape(title))
        ax_main_title.text(0.1, 1.75, title, font=fonts.yekan_extra_bold, size=20)
        plt.subplots_adjust(wspace=0, hspace=0)
        self.plot_values(xvals=dat, yvals=dat, title="", ax=ax_others)
        plt.show()

    def plot_values(self, xvals, yvals, title, ax):
        ax.imshow(self.logo_dailytahlil, aspect='auto', extent=(0, len(xvals), min(yvals) / 2, max(yvals) / 2),
                  alpha=0.1,
                  zorder=1)
        xvals = [xvals[i] for i in range(len(yvals)) if not (yvals[i] == np.inf or pd.isna(yvals[i]))]
        yvals = [i for i in yvals if not (i == np.inf or pd.isna(i))]
        xvals = [digits.en_to_fa(get_display(arabic_reshaper.reshape(str(i)))) for i in xvals]
        plt_title = title
        reshaped_text = arabic_reshaper.reshape(plt_title)
        artext = get_display(reshaped_text)
        position = np.arange(len(xvals))
        ax.bar(position, yvals, align='center', linewidth=0)
        for i in position:
            ax.axvline(x=i, ymin=-10 ** 30, ymax=10 ** 30, color='#e6e7e9', linewidth=30, alpha=1, zorder=-1)
        ax.set_xticks(position, xvals)
        ax.set_title(artext, font=fonts.yekan, loc='right', size=14, color='gray')
        ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='off')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(bottom=False, labelrotation=0, top=False, right=False, left=False)
        ylabels = ax.get_yticks()
        xlabels = ax.get_xticks()
        ylabels = [str(i) for i in ylabels]

        labels = [
            digits.en_to_fa(
                f"({i.replace('-', '').replace(' ', '')[:4]})" if '-' in i else i[:4])
            for
            i in ylabels]
        ylabels = [float(i) for i in ylabels]
        ax.set_yticks(ticks=ylabels, labels=labels, font=fonts.yekan_num)
        ax.set_xticks(ticks=xlabels, labels=xvals, font=fonts.yekan_num, rotation=90)

        # newax = fig.add_axes([0.8, 0.8, 0.2, 0.2], anchor='NE', zorder=1)
        # ax.axvline(x=np.mean(xlabels[len(xlabels) - 2:]), ymin=-1000, ymax=1000, linewidth=0.2, color='black')
        # ax.imshow(self.logo_dailytahlil, extent=[0, 3, -5, 5])

    def barplot_legend(self):
        pass


x = Plot()
x.grid_method()
x.logo_dailytahlil.resize()
