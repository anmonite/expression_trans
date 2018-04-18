#!/usr/bin/env python
# -*- coding: utf-8 -*-

class verbConjugate:
    def __init__(self, vorbose=False):
        # 入力用
        self.vorbose = vorbose
        self.word = ''
        self.word_after = ''
        self.fold = ''
        self.form = ''
        self.word_br = ''
        self.word_bs = ''
        self.word_gc = ''
        self.word_gp = ''
        self.word_gq = ''

        # 活用検索用
        self.char_A = ['あ', 'か', 'が', 'さ', 'ざ', 'た', 'だ', 'な', 'は', 'ば', 'ぱ', 'ま', 'や', 'ら', 'わ']
        self.char_I = ['い', 'き', 'ぎ', 'し', 'じ', 'ち', 'ぢ', 'に', 'ひ', 'び', 'ぴ', 'み', '－', 'り', 'い']
        self.char_U = ['う', 'く', 'ぐ', 'す', 'ず', 'つ', 'づ', 'ぬ', 'ふ', 'ぶ', 'ぷ', 'む', 'ゆ', 'る', 'う']
        self.char_E = ['え', 'け', 'げ', 'せ', 'ぜ', 'て', 'で', 'ね', 'へ', 'べ', 'ぺ', 'め', '－', 'れ', 'え']
        self.char_O = ['お', 'こ', 'ご', 'そ', 'ぞ', 'と', 'ど', 'の', 'ほ', 'ぼ', 'ぽ', 'も', 'よ', 'ろ', 'お']
        self.char_T = ['ん', 'っ']
        self.num_X = self.num_Y = 0

        # 結果用
        self.wordDic = ''
        self.PoW_MA = False    # 撥音便「ん」変換用：送り仮名 マ行
        self.process_log =''

        return None

    # print vorbose log with switching output std.out each part or only logging
    def printLog(self, *arg):
        if self.vorbose:
            print(*arg)

        self.process_log += str(*arg) + '\n'

        return self

    def Conjugate(self, word, after='*', fold='*', form='*'):
        # 入力単語
        self.word = word                    # 単語
        self.word_after = after             # 直後の用言
        self.word_br = word[:-1]            # 語幹(語尾１文字の場合)
        self.word_bs = word[:-2]            # 語幹(語尾２文字の場合)
        self.word_gc = word[-1:]            # 語尾(末尾)
        self.word_gp = word[-2:-1]          # 語尾(末尾の1つ前)
        self.word_gq = word[-3:-2]          # 語尾(末尾の2つ前)
        self.fold = fold                    # 活用型
        self.form = form.replace('形', '')  # 活用形

        self.printLog('Conjugate - %s(%s,%s形)+%s' % (word, fold, form, after))

        # 送り仮名の五十音上の行と段のチェック
        for n in range(0, 15):
            # X行
            if self.word_gc == self.char_U[n]:
                self.num_X = n

            # Y段
            if self.word_gp == self.char_I[n] or self.word_gp == self.char_E[n]:
                self.num_Y = n

        if fold.startswith('カ変') or fold.startswith('か変'):
            #カ行変格活用
            self.printLog('カ行変格活用')
            if form == '未然':
                if self.word_br == '来':
                    self.wordDic = self.word_br + ''
                else:
                    self.wordDic = 'こ'
            elif form == '連用':
                if self.word_br == '来':
                    self.wordDic = self.word_br + ''
                else:
                    self.wordDic = 'き'
            elif self.form == '終止' or self.form == '基本':
                if self.word_br == '来':
                    self.wordDic = self.word_br + 'る'
                else:
                    self.wordDic = 'くる'
            elif form == '連体':
                if self.word_br == '来':
                    self.wordDic = self.word_br + 'る'
                else:
                    self.wordDic = 'くる'
            elif form == '仮定':
                if self.word_br == '来':
                    self.wordDic = self.word_br + 'れ'
                else:
                    self.wordDic = 'くれ'
            elif form == '命令':
                if self.word_br == '来':
                    self.wordDic = self.word_br + 'い'
                else:
                    self.wordDic = 'こい'

        elif fold.startswith('サ変') or fold.startswith('さ変'):
            if self.word == 'する':
                #サ行変格活用
                self.printLog('サ行変格活用')
                if form == '未然':
                    self.wordDic = 'し'
                elif form == '連用':
                    self.wordDic = 'し'
                elif self.form == '終止' or self.form == '基本':
                    self.wordDic = 'する'
                elif form == '連体':
                    self.wordDic = 'する'
                elif form == '仮定':
                    self.wordDic = 'すれ'
                elif form == '命令':
                    self.wordDic = 'しろ'
            else:
                #ザ行変格活用(ザ行上一段活用)
                self.printLog('ザ行変格活用(ザ行上一段活用)')
                if form == '未然':
                    self.wordDic = self.word_bs + 'じ'
                elif form == '連用':
                    self.wordDic = self.word_bs + 'じ'
                elif self.form == '終止' or self.form == '基本':
                    self.wordDic = self.word_bs + self.word_gp + 'る'
                elif form == '連体':
                    self.wordDic = self.word_bs + self.word_gp + 'る'
                elif form == '仮定':
                    self.wordDic = self.word_bs + self.word_gp + 'れ'
                elif form == '命令':
                    self.wordDic = self.word_bs + 'じろ'

        elif fold.startswith('ザ変') or fold.startswith('ざ変'):
            #ザ行変格活用(ザ行上一段活用)
            self.printLog('ザ行変格活用(ザ行上一段活用)')
            if form == '未然':
                self.wordDic = self.word_bs + 'じ'
            elif form == '連用':
                self.wordDic = self.word_bs + 'じ'
            elif self.form == '終止' or self.form == '基本':
                self.wordDic = self.word_bs + self.word_gp + 'る'
            elif form == '連体':
                self.wordDic = self.word_bs + self.word_gp + 'る'
            elif form == '仮定':
                self.wordDic = self.word_bs + self.word_gp + 'れ'
            elif form == '命令':
                self.wordDic = self.word_bs + 'じろ'

        elif fold.startswith('五段'):
            self.conjugateGodan()

        elif fold.find('一段') != -1:
            # 上一段・下一段
            self.conjugateIchidan()

        else:
            pass

        return self.wordDic


    # 一段活用
    def conjugateIchidan(self):
        self.printLog('一段活用')

        if self.form == '未然':
            self.wordDic = self.word_br + ''

        elif self.form == '連用':
            self.wordDic = self.word_br + ''

        elif self.form == '終止' or self.form == '基本':
            self.wordDic = self.word_br + 'る'

        elif self.form == '連体':
            self.wordDic = self.word_br + 'る'

        elif self.form == '仮定':
            self.wordDic = self.word_br + 'れ'

        elif self.form == '命令':
            self.wordDic = self.word_br + 'ろ'

    # 五段活用
    def conjugateGodan(self):
        if self.form == '未然':
            if self.word_after == 'う':
                self.wordDic = self.word_br + self.char_O[self.num_X]
            else:
                self.wordDic = self.word_br + self.char_A[self.num_X]

        elif self.form == '連用':
            __first_part = '五段 %s行 ' % self.char_A[self.num_X]
            if((self.word in ['行く', 'いく', '蹴る', 'ける', '競る', '照る', 'てる']) or (self.char_A[self.num_X] in ['あ', 'た', 'ら', 'わ'])):
                if self.word_after == 'た' or self.word_after == 'て':
                    # 五段活用・促音便
                    self.printLog('%s促音便' % __first_part)
                    self.wordDic = self.word_br + 'っ'
                elif self.word_after != 'ます':
                    # 五段活用・イ音便
                    self.printLog('%sい音便' % __first_part)
                    self.wordDic = self.word_br + self.char_I[self.num_X]
                else:
                    self.wordDic = self.word_br + self.char_I[self.num_X]
            elif self.char_A[self.num_X] in ['ま', 'ば', 'な']:
                # 五段活用・撥音便
                self.printLog('%s撥音便' % __first_part)
                self.wordDic = self.word_br + 'ん'
                self.PoW_MA = True
            elif self.char_A[self.num_X] in ['か', 'が']:
                # 五段活用・カ行イ音便
                self.printLog('%sい音便' % __first_part)
                self.wordDic = self.word_br + 'い'
            elif self.char_A[self.num_X] == 'さ':
                # 五段活用・サ行イ音便
                self.printLog('%sい音便' % __first_part)
                self.wordDic = self.word_br + self.char_I[self.num_X]
            else:
                self.wordDic = self.word_br + self.char_I[self.num_X]

        elif self.form == '終止' or self.form == '基本':
            self.wordDic = self.word_br + self.char_U[self.num_X]

        elif self.form == '連体':
            self.wordDic = self.word_br + self.char_U[self.num_X]

        elif self.form == '仮定':
            self.wordDic = self.word_br + self.char_E[self.num_X]

        elif self.form == '命令':
            self.wordDic = self.word_br + self.char_E[self.num_X]


if __name__ == '__main__':
    import sys

    mode = False
    if len(sys.argv) == 1:
        mode = False
    elif sys.argv[1] == '-v':
        mode = True
    else:
        print('illigal option: -v - Output processing log.')
        exit()

    w = verbConjugate(mode)
    while True:
        __word = input('INPUT 動詞の基本(終止)形 (exit = n) > ')
        if __word == 'n':
            break

        __after = input('INPUT 動詞の直後の用言 (exit = n) > ')
        if __after == 'n':
            break

        __fold = input('INPUT 動詞の活用型(ex. 五段 一段) (exit = n) > ')
        if __fold == 'n':
            break

        __form = input('INPUT 動詞の活用形(ex. 連用 未然) (exit = n) > ')
        if __form == 'n':
            break

        print('%s (%s) : %s %s = %s (%s)' % (__word, __after, __fold, __form, w.Conjugate(__word, __after, __fold, __form), __after))
