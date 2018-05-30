#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import functools
import re

# import Sudachi tokenizer with using arranged UniDic and NEologd library
from sudachipy import config
from sudachipy import dictionary

# import verb cojugation module
from expression_trans.verb_conjugate.verb_conjugate import verbConjugate

class expressionTranslate:

    # constructor
    def __init__(self, vorbose=False, model_path='holo', instance=None):
        # for input
        self.model_path = model_path
        self.ModelsPath = os.path.dirname(__file__) + '/models/' + self.model_path
        self.vorbose = vorbose
        self.instance = instance

        # for works
        self.sudachi_settings = {}
        self.token = []
        self.tokens = []
        self.pos = 0
        self.strings = ''
        self.translated_strings = ''
        self.translated_tokens = []
        self.translated_surface_list = []
        self.translated_log = ''
        self.add_fetch_count = 0

        # for token processing
        # IPA dictionary item order "surface\tPoS,c1,c2,c3,type,form[,\t]origin[,\t]read,pron"
        self.pattern = re.compile(r'[\t,]')
        self.elements = []
        self.surface = ''
        self.PoS = ''
        self.c1 = ''
        self.c2 = ''
        self.c3 = ''
        self.fold = ''
        self.form = ''
        self.origin = ''
        self.read = ''
        self.pron = ''

        # for analize auxialiry verb
        self.pattern_end = re.compile(r'[。、\,\.？！\?\!\s]')
        self.pre_token = []
        self.after_token = []
        self.next_list_token = []

        # for output
        self.translated_text = ''
        self.process_log = ''

        # sort dictionary by length of keyword (UTF-8) by decending
        def keylength_cmp(x, y):
            a = len(x)
            b = len(y)
            return b - a

        # loading honorific translation table
        self.honorific_sorted_list = {}
        try:
            with open('%s/conv_honorific.json' % self.ModelsPath, 'r') as f:
                honorific_data = json.load(f)
                honorific_list = list(honorific_data.items())
                # sort by key string length as decending order
                self.honorific_sorted_list = sorted(honorific_list, key=functools.cmp_to_key(lambda a, b: keylength_cmp(a[0], b[0])))
        except json.JSONDecodeError as err:
            print('honorific translation JSON loading Error: {0}'.format(err))

        # loading specific translation table
        self.specific_sorted_list = {}
        try:
            with open('%s/conv_specific.json' % self.ModelsPath, 'r') as f:
                specific_data = json.load(f)
                specific_list = list(specific_data.items())
                # sort by key string length as decending order
                self.specific_sorted_list = sorted(specific_list, key=functools.cmp_to_key(lambda a, b: keylength_cmp(a[0], b[0])))
        except json.JSONDecodeError as err:
            print('specific translation JSON loading Error: {0}'.format(err))

        # loading noun translation table
        self.noun_sorted_list = {}
        try:
            with open('%s/conv_noun.json' % self.ModelsPath, 'r') as f:
                noun_data = json.load(f)
                noun_list = list(noun_data.items())
                # sort by key string length as decending order
                self.noun_sorted_list = sorted(noun_list, key=functools.cmp_to_key(lambda a, b: keylength_cmp(a[0], b[0])))
        except json.JSONDecodeError as err:
            print('noun translation JSON loading Error: {0}'.format(err))

        # loading interjection translation table
        self.interjection_sorted_list = {}
        try:
            with open('%s/conv_interjection.json' % self.ModelsPath, 'r') as f:
                interjection_data = json.load(f)
                interjection_list = list(interjection_data.items())
                # sort by key string length as decending order
                self.interjection_sorted_list = sorted(interjection_list, key=functools.cmp_to_key(lambda a, b: keylength_cmp(a[0], b[0])))
        except json.JSONDecodeError as err:
            print('interjection translation JSON loading Error: {0}'.format(err))

        # loading adjective translation table
        self.adjective_list = {}
        try:
            with open('%s/conv_adjective.json' % self.ModelsPath, 'r') as f:
                adjective_data = json.load(f)
                self.adjective_list = list(adjective_data.items())
        except json.JSONDecodeError as err:
            print('adjective translation JSON loading Error: {0}'.format(err))

        # loading after adjective translation table
        self.afteradjective_list = {}
        try:
            with open('%s/conv_afteradjective.json' % self.ModelsPath, 'r') as f:
                afteradjective_data = json.load(f)
                self.afteradjective_list = list(afteradjective_data.items())
        except json.JSONDecodeError as err:
            print('after adjective translation JSON loading Error: {0}'.format(err))

        # loading adverb translation table
        self.adverb_sorted_list = {}
        try:
            with open('%s/conv_adverb.json' % self.ModelsPath, 'r') as f:
                adverb_data = json.load(f)
                adverb_list = list(adverb_data.items())
                # sort by key string length as decending order
                self.adverb_sorted_list = sorted(adverb_list, key=functools.cmp_to_key(lambda a, b: keylength_cmp(a[0], b[0])))
        except json.JSONDecodeError as err:
            print('adverb translation JSON loading Error: {0}'.format(err))

        # loading particle translation table
        self.particle_sorted_list = {}
        try:
            with open('%s/conv_particle.json' % self.ModelsPath, 'r') as f:
                particle_data = json.load(f)
                particle_list = list(particle_data.items())
                # sort by key string length as decending order
                self.particle_sorted_list = sorted(particle_list, key=functools.cmp_to_key(lambda a, b: keylength_cmp(a[0], b[0])))
        except json.JSONDecodeError as err:
            print('particle translation JSON loading Error: {0}'.format(err))

        # loading auxverb translation table
        self.auxverb_sorted_list = {}
        try:
            with open('%s/conv_auxverb.json' % self.ModelsPath, 'r') as f:
                auxverb_data = json.load(f)
                auxverb_list = list(auxverb_data.items())
                # sort by key string length as decending order
                self.auxverb_sorted_list = sorted(auxverb_list, key=functools.cmp_to_key(lambda a, b: keylength_cmp(a[1], b[1])))
        except json.JSONDecodeError as err:
            print('auxverb translation JSON loading Error: {0}'.format(err))

        # loading last verb translation table
        self.lastverb_list = {}
        try:
            with open('%s/conv_lastverb.json' % self.ModelsPath, 'r') as f:
                lastverb_data = json.load(f)
                self.lastverb_list = list(lastverb_data.items())
        except json.JSONDecodeError as err:
            print('last verb translation JSON loading Error: {0}'.format(err))

        return None

    def __del__(self):
        # for input
        self.model_path = ''
        self.ModelsPath = ''
        self.vorbose = False
        self.instance = None

        # for works
        self.sudachi_settings = {}
        self.token = []
        self.tokens = []
        self.pos = 0
        self.strings = ''
        self.translated_strings = ''
        self.translated_tokens = []
        self.translated_surface_list = []
        self.translated_log = ''
        self.add_fetch_count = 0

        # for token processing
        self.pattern = ''
        self.elements = []
        self.surface = ''
        self.PoS = ''
        self.c1 = ''
        self.c2 = ''
        self.c3 = ''
        self.fold = ''
        self.form = ''
        self.origin = ''
        self.read = ''
        self.pron = ''

        # for analize auxialiry verb
        self.pattern_end = ''
        self.pre_token = []
        self.after_token = []
        self.next_list_token = []

        # for output
        self.translated_text = ''
        self.process_log = ''

        return None


    # contain methods

    # remove unexpected control code
    def removeCtrlCode(self, text):
        __safety_text = ''
        for c in text:
            ord_num = ord(c)
            if ord_num < 0x20 or (ord_num >= 0x7f and ord_num <= 0xff) or (ord_num >= 0xc280 and ord_num <= 0xc2a0):
                # remove code 0x00 - 0x1F or 0x7F - 0xFF or 0xC280 - 0xC2A0
                continue
            else:
                __safety_text += c

        return __safety_text

    # print vorbose log with switching output std.out each part or only logging
    def printLog(self, *arg):
        if self.vorbose:
            print(*arg)

        self.process_log += str(*arg) + '\n'

        return self

    # get each analized elements from token line
    def splitToken(self, token):
        """
        .. py:classmethod:: splitToken(self, token)

            get each analized elements from token line
        """

        self.elements = re.split(r'[\t,]', token)
        self.surface = self.elements[0]
        self.PoS = self.elements[1]
        self.c1 = self.elements[2]
        self.c2 = self.elements[3]
        self.c3 = self.elements[4]
        self.fold = self.elements[5]
        self.form = self.elements[6]
        self.origin = self.elements[7]
        self.read = self.elements[8]
        self.pron = self.elements[9]

        return self

    # execute Sudachi tokenizer
    def execSudachiTokenizer(self, text):
        """ execute Sudachi tokenizer """

        #exec tokenizer
        for self.tokens in self.instance.tokenize('C', text):
            __list_info = [
                self.tokens.surface(),
                ",".join(self.tokens.part_of_speech()),
                self.tokens.normalized_form()]
            __list_info += [self.tokens.dictionary_form(), self.tokens.reading_form()]
            if self.tokens.is_oov():
                __list_info.append("(OOV)")
            self.translated_tokens.append("\t".join(__list_info))
            self.translated_log += '> ' + "\t".join(__list_info) + '\n'

        return self

    # translate honorific words (execute to strings)
    def traslateHonorific(self, text):
        if self.honorific_sorted_list == {}:
            return self

        self.translated_strings = text
        for j in range(len(self.honorific_sorted_list)):
            if text.find(self.honorific_sorted_list[j][0]) == -1:
                continue
            else:
                self.translated_strings = text.replace(self.honorific_sorted_list[j][0], self.honorific_sorted_list[j][1])
                self.translated_log += 'Found keyword: "' + self.honorific_sorted_list[j][0] + '"\n'
                self.translated_log += 'Translated: ' + self.honorific_sorted_list[j][1] + '\n'
                text = self.translated_strings
        return self

    # translate specific words (execute to strings)
    def traslateSpecific(self, text):
        if self.specific_sorted_list == {}:
            return self

        self.translated_strings = text
        for j in range(len(self.specific_sorted_list)):
            if text.find(self.specific_sorted_list[j][0]) == -1:
                continue
            else:
                self.translated_strings = text.replace(self.specific_sorted_list[j][0], self.specific_sorted_list[j][1])
                self.translated_log += 'Found keyword: "' + self.specific_sorted_list[j][0] + '"\n'
                self.translated_log += 'Translated: ' + self.specific_sorted_list[j][1] + '\n'
                text = self.translated_strings
        return self

    # translate noun token (execute to token strings)
    def traslateNoun(self, token):
        self.token = self.splitToken(token)
        self.translated_log = ''
        __surface = self.token.surface

        if self.noun_sorted_list == {}:
            return __surface

        for j in range(len(self.noun_sorted_list)):
            if token.find(self.noun_sorted_list[j][0]) == -1:
                __surface = self.token.surface
                continue
            else:
                __surface = self.surface.replace(self.noun_sorted_list[j][0], self.noun_sorted_list[j][1])
                self.translated_log += 'Found keyword: "' + self.noun_sorted_list[j][0] + '"\n'
                self.translated_log += 'Translated: ' + __surface
                self.add_fetch_count = 0
                break
        return __surface

    # translate interjection token (execute to token strings)
    def traslateInterjection(self, token):
        self.token = self.splitToken(token)
        self.translated_log = ''
        __surface = self.token.surface

        if self.interjection_sorted_list == {}:
            return __surface

        for j in range(len(self.interjection_sorted_list)):
            if token.find(self.interjection_sorted_list[j][0]) == -1:
                continue
            else:
                __surface = self.surface.replace(self.interjection_sorted_list[j][0], self.interjection_sorted_list[j][1])
                self.translated_log += 'Found keyword: "' + self.interjection_sorted_list[j][0] + '"\n'
                self.translated_log += 'Translated: ' + __surface
                self.add_fetch_count = 0
                break
        return __surface

    # translate adjective token (execute to token)
    def traslateAdjective(self, token, pos, max_pos):
        self.pos = pos
        self.token = self.splitToken(token)
        self.translated_log = ''
        __surface = self.token.surface
        __surface_org = self.token.surface
        __form = self.token.form

        if (self.adjective_list == {}) and (self.afteradjective_list == {}):
            self.add_fetch_count = 0
            return __surface

        # simple translation for adjective
        if self.adjective_list != {}:
            for j in range(len(self.adjective_list)):
                if token.find(self.adjective_list[j][0]) == -1:
                    continue
                else:
                    __surface = self.surface.replace(self.adjective_list[j][0], self.adjective_list[j][1])
                    self.translated_log += 'Found keyword: "' + self.adjective_list[j][0] + '"\n'
                    self.translated_log += 'Translated: ' + __surface
                    self.add_fetch_count = 0
                    break
            __surface_org = __surface

        if pos == max_pos-1:
            self.add_fetch_count = 0
            return __surface_org

        # not last token but next word is ending symbol or not
        self.after_token = self.splitToken(self.translated_tokens[pos + 1])
        __after_surface = self.after_token.surface
        __after_PoS = self.after_token.PoS
        __after_form = self.after_token.PoS

        # return if current position is last word
        if re.match(self.pattern_end, __after_surface):
            self.add_fetch_count = 0
            return __surface_org

        # handling a word after adjective
        __surface = __surface_org
        for j in range(len(self.afteradjective_list)):
            if __form.find(self.afteradjective_list[j][0]) == -1:
                continue
            else:
                # insert the word after specific adjective
                if __after_surface == self.afteradjective_list[j][1][0]:
                    __surface = __surface_org + self.afteradjective_list[j][1][1]
                    self.translated_log += 'Found keyword: "' + __surface_org + '"\n'
                    self.translated_log += 'Translated: ' + __surface
                    break

        self.add_fetch_count = 0
        return __surface

    # translate adverb token (execute to token strings)
    def traslateAdverb(self, token):
        self.token = self.splitToken(token)
        self.translated_log = ''
        __surface = self.token.surface

        if self.adverb_sorted_list == {}:
            return __surface

        for j in range(len(self.adverb_sorted_list)):
            if token.find(self.adverb_sorted_list[j][0]) == -1:
                continue
            else:
                __surface = self.surface.replace(self.adverb_sorted_list[j][0], self.adverb_sorted_list[j][1])
                self.translated_log += 'Found keyword: "' + self.adverb_sorted_list[j][0] + '"\n'
                self.translated_log += 'Translated: ' + __surface
                self.add_fetch_count = 0
                break
        return __surface

    # translate particle token (execute to token strings)
    def traslateParticle(self, token):
        self.token = self.splitToken(token)
        self.translated_log = ''
        __surface = self.token.surface

        if self.particle_sorted_list == {}:
            return __surface

        for j in range(len(self.particle_sorted_list)):
            if token.find(self.particle_sorted_list[j][0]) == -1:
                continue
            else:
                __surface = self.surface.replace(self.particle_sorted_list[j][0], self.particle_sorted_list[j][1])
                self.translated_log += 'Found keyword: "' + self.particle_sorted_list[j][0] + '"\n'
                self.translated_log += 'Translated: ' + __surface
                self.add_fetch_count = 0
                break
        return __surface

    # translate auxiliary verb token (execute to multiple tokens)
    def traslateAuxverb(self, token, pos, max_pos):
        self.pos = pos
        self.token = self.splitToken(token)
        self.translated_log = ''
        __surface = self.token.surface
        __surface_org = self.token.surface
        __original_verb = ''
        __formed_verb = ''

        if self.auxverb_sorted_list == {}:
            return __surface

        self.pre_token = self.splitToken(self.translated_tokens[self.pos - 1])
        __pre_surface = self.pre_token.surface
        __pre_PoS = self.pre_token.PoS
        __pre_read = self.pre_token.read
        __pre_fold = self.pre_token.fold

        # nothing to do if before token is auxialiry verb and it's surface is not "らしい"
        if __pre_PoS == '助動詞' and __pre_surface != 'らしい':
            self.surface = __surface_org
            return self

        # check succeeding words
        self.after_token = self.splitToken(self.translated_tokens[self.pos + 1])
        __after_surface = self.after_token.surface
        __after_PoS = self.after_token.PoS
        __after_c1 = self.after_token.c1

        # add "ん" after auxialiry verb is "らしい" if succeeding word is "です" or "だ"
        if __surface_org == 'らしい' and __after_PoS == '助動詞' and __after_surface.find(['です', 'だ']) != -1:
            __surface = __surface_org + 'ん'
            __surface_org = __surface

        # loop of auxverb keyword patterns to replace
        for j in range(len(self.auxverb_sorted_list)):
            if __surface_org != self.auxverb_sorted_list[j][0]:
                continue
            else:
                # check matching of succeeding words(particle or symbol char) pattern

                # make connected strings of token surface in list
                __next_list_token = list(self.auxverb_sorted_list[j][1].items())
                __next_list_strings = ''
                __next_strings = ''
                __num_next_list_words = 0
                __succeeding_list_pos = 0

                for i in range(0, len(__next_list_token)):
                    __trans_list = re.split(r',', __next_list_token[i][0])
                    __next_list_strings = re.sub(r',', '', ''.join(__trans_list))    # pattern words
                    __num_next_list_words = len(__trans_list)

                    # make connected strings after current position in text
                    __next_words = ''
                    __max_pos = max_pos if ((self.pos + 1 + __num_next_list_words) > max_pos) else (self.pos + 1 + __num_next_list_words)
                    for k in range(self.pos + 1, __max_pos):
                        # check succeeding words
                        self.after_token = self.splitToken(self.translated_tokens[self.pos + 1])
                        __after_surface = self.after_token.surface
                        __after_PoS = self.after_token.PoS
                        __after_c1 = self.after_token.c1

                        __next_words += self.splitToken(self.translated_tokens[k]).surface

                        # break if succeeding word is an ending symbol nor a conjunctive particle
                        if re.match(self.pattern_end, __after_surface) or (__after_PoS == '助詞' and __after_c1 == '接続助詞'):
                            break

                    if __next_list_strings == __next_words:
                        __next_strings = __next_list_strings
                        __succeeding_list_pos = i
                        break

                # no match in succeeding words
                if __next_strings == '':
                    self.surface = __surface_org
                    return self

                # change verb's form if there is a verb just before this auxiliary verb
                v_conjugate = verbConjugate()
                if __pre_PoS == '動詞':
                    if((__surface_org == 'ましょ') or (__surface_org == 'ます')):
                        __original_verb = __pre_surface
                        __formed_verb = v_conjugate.Conjugate(__pre_read, __surface_org, __pre_fold, '終止')
                    elif __surface_org == 'まし':
                        __original_verb = __pre_surface
                        __formed_verb = v_conjugate.Conjugate(__pre_read, __surface_org, __pre_fold, '連用')
                        self.translated_log += ("__formed_verb - %s\n" % __formed_verb)
                    else:
                        __original_verb = __pre_surface
                        __formed_verb = __pre_surface

                    # replace the last verb token surface string
                    self.translated_surface_list[self.pos - 1] = __formed_verb

                # replace sueface pattern strings of this auxuialiry verb
                __surface = __next_list_token[__succeeding_list_pos][1]

                # 動詞五段活用・マ行+「まし」+「た+」 > 「ん」+「だ+」
                if v_conjugate.PoW_MA:
                    __surface = re.sub(r'た', 'だ', __surface)

                self.translated_log += 'Found keyword: ({0})+{1}+{2}\n'.format(__original_verb, __surface_org, __next_strings)
                self.translated_log += 'Translated: ({0})+{1}'.format(__formed_verb, __surface)
                self.add_fetch_count = __num_next_list_words
                break

        self.surface = __surface
        return self

    # translate (last)verb token (execute to multiple tokens)
    def traslateLastverb(self, token, pos, max_pos):
        self.pos = pos
        self.token = self.splitToken(token)
        self.translated_log = ''
        __surface = self.token.surface
        __surface_org = self.token.surface
        __fold = self.token.fold
        __form = self.token.form
        __read = self.token.read

        if self.lastverb_list == {}:
            self.add_fetch_count = 0
            return __surface_org

        # last position?
        if pos < max_pos-1:
            self.after_token = self.splitToken(self.translated_tokens[pos + 1])
            __after_surface = self.after_token.surface

            # 五段活用(イ音便以外)+連用形+「ます」
            if((__fold.find('五段') != -1) and (__fold.find('イ音便') == -1) and (__form.find('連用') != -1) and __after_surface == 'ます'):
                __surface = __surface_org + 'んす'
                self.translated_log += 'Found keyword: "' + __surface_org + '"\n'
                self.translated_log += 'Translated: ' + __surface
                self.add_fetch_count = 1
            else:
                # not last token but succeeding word is ending symbol or not
                if not re.match(self.pattern_end, __after_surface):
                    self.add_fetch_count = 0
                    return __surface_org

                # 五段活用・イ音便+連用形+「ます」
                if(((__fold.find('五段') != -1) and (__fold.find('イ音便') != -1)) or (__fold.find('一段') != -1)):
                    __surface = __surface_org + 'んじゃ'
                    self.translated_log += 'Found keyword: "' + __surface_org + '"\n'
                    self.translated_log += 'Translated: ' + __surface
                    self.add_fetch_count = 0

                else:
                    __surface = __surface_org
                    for j in range(len(self.lastverb_list)):
                        # verb's form check
                        if __form != self.lastverb_list[j][0]:
                            continue
                        else:
                            v_conjugate = verbConjugate()
                            __formed_verb = v_conjugate.Conjugate(__surface_org, '', __fold, self.lastverb_list[j][1][0])
                            __surface = __formed_verb + self.lastverb_list[j][1][1]
                            self.translated_log += 'Found keyword: "' + __surface_org + '"\n'
                            self.translated_log += 'Translated: ' + __surface
                            break
                    self.add_fetch_count = 0

        elif pos == max_pos-1:
            if(((__fold.find('五段') != -1) and (__fold.find('イ音便') != -1)) or (__fold.find('一段') != -1)):
                __surface = __surface_org + 'んじゃ'
                self.translated_log += 'Found keyword: "' + __surface_org + '"\n'
                self.translated_log += 'Translated: ' + __surface
                self.add_fetch_count = 0

            else:
                __surface = __surface_org
                for j in range(len(self.lastverb_list)):
                    # verb's form check
                    if __form != self.lastverb_list[j][0]:
                        continue
                    else:
                        v_conjugate = verbConjugate()
                        __formed_verb = v_conjugate.Conjugate(__surface_org, '', __fold, self.lastverb_list[j][1][0])
                        __surface = __formed_verb + self.lastverb_list[j][1][1]
                        self.translated_log += 'Found keyword: "' + __surface_org + '"\n'
                        self.translated_log += 'Translated: ' + __surface
                        break
                self.add_fetch_count = 0

        return __surface

    # translate whole text (execute to strings)
    def translateText(self, text):
        __tokens = []
        __original_text = text

        # remove unexpected char
        __clean_text = self.removeCtrlCode(__original_text)

        # nomalization hankaku symbol to Zenkaku
        __normalized_text = __clean_text.replace('?', '？')
        __normalized_text = __normalized_text.replace('!', '！')

        self.printLog('-----')

        self.translated_log = ''
        self.printLog('Translate honorific words: ')
        self.printLog('-----')
        __text = self.traslateHonorific(__normalized_text).translated_strings
        if self.translated_log == '':
            self.printLog('Nothing to translate in text.')
        else:
            self.printLog(self.translated_log)
        self.printLog('-----\n')

        self.translated_log = ''
        self.printLog('Translate specific words: ')
        self.printLog('-----')
        __text = self.traslateSpecific(__text).translated_strings
        if self.translated_log == '':
            self.printLog('Nothing to translate in text.')
        else:
            self.printLog(self.translated_log)
        self.printLog('-----\n')

        self.translated_log = ''
        self.printLog('Morphological analisis after replacement: ')
        self.printLog('-----')
        __tokens = self.execSudachiTokenizer(__text).translated_tokens
        self.printLog(self.translated_log)
        self.printLog('-----')

        self.translated_surface_list = []
        self.translated_log = ''

        __pos = 0
        __max_pos = len(__tokens)
        while __pos < __max_pos:
            self.token = self.splitToken(__tokens[__pos])
            self.printLog('%s: %s' % (__pos, __tokens[__pos]))
            __translated = self.token.surface

            if self.token.PoS == '名詞' or self.token.PoS == '代名詞':
                __translated = self.traslateNoun(__tokens[__pos])
                if self.translated_log != '':
                    self.printLog(self.translated_log)
                self.translated_surface_list.append(__translated)
                if self.token.surface != __translated:
                    self.printLog('Translate noun token: %s > %s\n' % (self.token.surface, __translated))
                else:
                    self.printLog('Nothing to translate: %s > %s\n' % (self.token.surface, self.token.surface))
                __pos += 1

            elif self.token.PoS == '感動詞':
                __translated = self.traslateInterjection(__tokens[__pos])
                if self.translated_log != '':
                    self.printLog(self.translated_log)
                self.translated_surface_list.append(__translated)
                if self.token.surface != __translated:
                    self.printLog('Translate interjection token: %s > %s\n' % (self.token.surface, __translated))
                else:
                    self.printLog('Nothing to translate: %s > %s\n' % (self.token.surface, self.token.surface))
                __pos += 1

            elif self.token.PoS == '形容詞':
                __current_surface = __translated
                __translated = self.traslateAdjective(__tokens[__pos], __pos, __max_pos)
                if self.translated_log != '':
                    self.printLog(self.translated_log)
                self.translated_surface_list.append(__translated)

                if __current_surface != __translated:
                    self.printLog('Translate adjective token: %s > %s\n' % (__current_surface, __translated))
                else:
                    self.printLog('Nothing to translate: %s > %s\n' % (__current_surface, __current_surface))

                # fetch amount succeeding word length
                __pos += 1

            elif self.token.PoS == '副詞':
                __translated = self.traslateAdverb(__tokens[__pos])
                if self.translated_log != '':
                    self.printLog(self.translated_log)
                self.translated_surface_list.append(__translated)
                if self.token.surface != __translated:
                    self.printLog('Translate adverb token: %s > %s\n' % (self.token.surface, __translated))
                else:
                    self.printLog('Nothing to translate: %s > %s\n' % (self.token.surface, self.token.surface))
                __pos += 1

            elif self.token.PoS == '助詞':
                __translated = self.traslateParticle(__tokens[__pos])
                if self.translated_log != '':
                    self.printLog(self.translated_log)
                self.translated_surface_list.append(__translated)
                if self.token.surface != __translated:
                    self.printLog('Translate particle token: %s > %s\n' % (self.token.surface, __translated))
                else:
                    self.printLog('Nothing to translate: %s > %s\n' % (self.token.surface, self.token.surface))
                __pos += 1

            elif self.token.PoS == '助動詞':
                __current_surface = __translated
                __translated = self.traslateAuxverb(__tokens[__pos], __pos, __max_pos).surface
                if self.translated_log != '':
                    self.printLog(self.translated_log)
                self.translated_surface_list.append(__translated)

                __succeeding_surface_list = ''
                for offset in range(__pos+1, __pos+self.add_fetch_count+1):
                    __succeeding_surface_list += self.splitToken(__tokens[offset]).surface

                if __current_surface != __translated:
                    self.printLog('Translate auxiliary verb token: %s > %s\n' % (__current_surface+__succeeding_surface_list, __translated))
                else:
                    self.printLog('Nothing to translate: %s > %s\n' % (__current_surface, __current_surface))

                # fetch amount succeeding word length
                __pos += 1 + self.add_fetch_count

            elif self.token.PoS == '動詞':
                __current_surface = __translated
                __translated = self.traslateLastverb(__tokens[__pos], __pos, __max_pos)
                if self.translated_log != '':
                    self.printLog(self.translated_log)
                self.translated_surface_list.append(__translated)
                if self.token.surface != __translated:
                    self.printLog('Translate (last)verb token: %s > %s\n' % (__current_surface, __translated))
                else:
                    self.printLog('Nothing to translate: %s > %s\n' % (__current_surface, __current_surface))
                __pos += 1 + self.add_fetch_count

            else:
                self.translated_surface_list.append(__translated)
                self.translated_log += __translated
                self.printLog('Nothing to translate: %s > %s\n' % (self.token.surface, __translated))
                __pos += 1

        self.translated_text = ''.join(self.translated_surface_list)
        return self


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

    # token analizer by Sudachi
    with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
        __sudachi_settings = json.load(f)

    # init dictionary
    __dict = dictionary.Dictionary(__sudachi_settings)
    __instance = __dict.create()

    while True:
        input_text = input('INPUT TEXT (exit = n) > ')
        if input_text == 'n':
            break

        original_text = input_text

        # init instance
        t = expressionTranslate(mode, 'holo', __instance)

        print('\nOriginal text: \n-----\n%s\n-----\n' % original_text)

        # translate whole text
        translated_text = t.translateText(original_text).translated_text
        if mode is False:
            print('Processing log: \n%s-----' % t.process_log)

        print('\nTranslated text: \n-----\n%s\n-----\n' % translated_text)
