import numpy as np
from matplotlib import pyplot as plt, gridspec
from pathlib import Path
import imageio as iio
import arabic_reshaper
from persiantools import digits
from bidi.algorithm import get_display
import pandas as pd


def cast_to_int(value):
    return int(round(value))


rows = {
    1: type('Dimension', (), {"height": 0.1, 'width': [0.29, 0.6]}),
    2: type('Dimension', (), {"height": 0.2, 'width': []}),
    3: type('Dimension', (), {"height": 0.25, 'width': [0.15, 0.3]}),
    4: type('Dimension', (), {"height": 0.70, 'width': []}),
    5: type('Dimension', (), {"height": 0.75, 'width': [0.15, 0.3]}),
    6: type('Dimension', (), {"height": 1, 'width': []}),
}

dat = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7]


def remove_axis(ax0):
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['left'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.set_xticks([])
    ax0.set_yticks([])
    ax0.set_anchor('W')
    return ax0


class Plot:

    def __init__(self, width=1080, height=1920):
        self.gs = None
        self.width = width
        self.height = height
        self.yekan_thin = Path("utils/fonts/iranyekan/YEKAN BAKH FA 02 THIN.TTF")
        self.yekan_light = Path("utils/fonts/iranyekan/YEKAN BAKH FA 03 LIGHT.TTF")
        self.yekan_regular = Path("utils/fonts/iranyekan/YEKAN BAKH FA 04 REGULAR.TTF")
        self.yekan_medium = Path("utils/fonts/iranyekan/YEKAN BAKH FA 05 MEDIUM.TTF")
        self.yekan_bold = Path("utils/fonts/iranyekan/YEKAN BAKH FA 06 BOLD.TTF")
        self.yekan_heavy = Path("utils/fonts/iranyekan/YEKAN BAKH FA 07 HEAVY.TTF")
        self.yekan_fat = Path("utils/fonts/iranyekan/YEKAN BAKH FA 08 FAT.TTF")
        self.logo_tadbirgaran = iio.imread("utils/img/logo_daily_tahlil.png")
        self.logo_dailytahlil = iio.imread("utils/img/logo_kargozari.png")

    def grid_method(self):
        self.gs = gridspec.GridSpec(self.width, self.height, wspace=0, hspace=0, )
        ax_daily_tahlil_logo = plt.subplot(
            self.gs[:cast_to_int(rows[1].height * self.height), :cast_to_int(rows[1].width[0] * self.width)])

        ax_tadbirgaran_logo = plt.subplot(
            self.gs[:cast_to_int(rows[1].height * self.height),
            cast_to_int((rows[1].width[0] + 0.02) * self.width):cast_to_int(rows[1].width[1] * self.width)])
        ax_main_title = plt.subplot(
            self.gs[:cast_to_int(rows[1].height * self.height), cast_to_int(rows[1].width[1] * self.width):])

        ax_others = plt.subplot(
            self.gs[cast_to_int(rows[1].height * self.height):, :])

        ax_daily_tahlil_logo = remove_axis(ax_daily_tahlil_logo)
        ax_tadbirgaran_logo = remove_axis(ax_tadbirgaran_logo)
        ax_main_title = remove_axis(ax_main_title)

        ax_daily_tahlil_logo.imshow(self.logo_dailytahlil)
        ax_tadbirgaran_logo.imshow(self.logo_tadbirgaran)
        title = "این یک متن تست است." + "(ُ1401/10/07)"
        title = digits.en_to_fa(title)
        title = get_display(arabic_reshaper.reshape(title))
        ax_main_title.text(0.33, 1.25, title, font=self.yekan_bold, size=12)
        plt.subplots_adjust(wspace=0, hspace=0)
        self.plot_values(xvals=dat, yvals=dat, title="سجاد", ax=ax_others)

        plt.show()

    def plot_values(self, xvals, yvals, title, ax):
        xvals = [xvals[i] for i in range(len(yvals)) if not (yvals[i] == np.inf or pd.isna(yvals[i]))]
        yvals = [i for i in yvals if not (i == np.inf or pd.isna(i))]
        xvals = [digits.en_to_fa(get_display(arabic_reshaper.reshape(str(i)))) for i in xvals]
        plt_title = title
        reshaped_text = arabic_reshaper.reshape(plt_title)
        artext = get_display(reshaped_text)
        position = np.arange(len(xvals))
        mybars = ax.bar(position, yvals, align='center', linewidth=0)
        ax.set_xticks(position, xvals)
        ax.set_title(artext, font=self.yekan_regular, loc='right', size=14, color='gray')
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
        ax.set_yticks(ticks=ylabels, labels=labels, font=self.yekan_regular)
        ax.set_xticks(ticks=xlabels, labels=xvals, font=self.yekan_regular, rotation=90)
        for i in ylabels:
            ax.axhline(y=i, xmin=-10, xmax=2, color='gray', linewidth=0.1, )
        ax.axvline(x=np.mean(xlabels[len(xlabels) - 2:]), ymin=-1000, ymax=1000, linewidth=0.2, color='black')

    def barplot_legend(self):
        pass


x = Plot()
x.grid_method()
