#!/usr/bin/env python2

import random, time, os
import pygame.midi as midi

###################################################################################
##                                                                               ##
##  Markovian Chant employs Markov chains and Pygame.midi in order to            ##
##  procedurally generate pseudo-Gregorian chant in the 6th Mode. The 6th        ##
##  Gregorian mode contains some of the more recognisable melodies from the      ##
##  Gregorian repertoire, such as the "Requiem aeternam" Intoit, the Agnus Dei   ##
##  from the "Missa de angelis" and the "Regina caeli" Antiphon.                 ##
##                                                                               ##
###################################################################################

midi.init()

if os.name == 'posix':
    player = midi.Output(2) #two works in Linux, but not 0 which was the default output
else:
    player = midi.Output(midi.get_default_output_id()) #device_id, latency, buffer_size

#player.set_instrument(100, 1) #instrument_id=value between 0 and 127, channel
player.set_instrument(48, 1) #instrument_id=value between 0 and 127, channel

print 'default output id', midi.get_default_output_id()
    #returns 0
print 'device info', midi.get_device_info(0)
    #returns ('ALSA', 'Midi Through Port-0', 0, 1, 1) = (interface, name, input?, output?, opened?)
print 'device info', midi.get_device_info(1)
print 'device info', midi.get_device_info(2)
print 'device info', midi.get_device_info(3)

starting_order = 4


NOTES = { \
            'a': 58, \
            'b': 60, \
            'c': 61, \
            'd': 63, \
            'e': 65, \
            'f': 66, \
            'g': 68, \
            'h': 70, \
            '!': 71, \
            'i': 72, \
            'j': 73, \
            'k': 75, \
            'l': 77, \
            'm': 78, \
        }

# Mode VI melodies
# introit_requiem is for example the introit 'Requiem aeternam'
# ! = ixi
VI = { \
      'introit_requiem' : 'f_fgfffgh_hggfgg.f.fgh_hghhjhgh!hgffgh_gfgg.f.hghgfhghgff.hghhjhgh!hgfgh_gfgg.f.fggfghhhhhhgh.fghhhhhhhhg!gh.fghhhhhhhhh.hhhhfghgff.f_fgfffgh_hggfgg.f.fgh_hghhjhgh!hgffgh_gfgg.f.hghgfhghgff.hghhjhgh!hgfgh_gfgg.f.', \
\
      'kyrie_requiem' : 'fgh!hh.g.hgfefgff.fgh!hh.g.hgfefgff.fgh!hh.g.hgfefgff.fgh!h.g.hgfefgff.fgh!h.g.hgfefgff.fgh!h.g.hgfefgff.fgh!hh.g.hgfefgff.fgh!hh.g.hgfefgff.jff.j!jkj!hg.hgfefgff.', \
\
      'resp_ne_recorderis' : 'dcffgh_hggfgg.f.fdfg!h!hg!.h!j_!hfgg.h!ghfdf_h_g_g.f.fhhghf_hghffdffgefgfdeddc.fghgh!hh.hjhggh!_hgfgh_gfgg.f.fg!_!!_h_!hgh_g_h!j_kjj!h!ghgfeghg.f.cdfffghffefg!_!_g_h!_hgghgfg.f.dcffgh_hggfgg.f.fdfg!h!hg!.h!j_!hfgg.h!ghfdf_h_g_g.f.fhhghf_hghffdffgefgfdeddc.fghgh!hh.hjhggh!_hgfgh_gfgg.f.fg!_!!_h_!hgh_g_h!j_kjj!h!ghgfeghg.f.cdfffghffefg!_!_g_h!_hgghgfg.f.', \
\
      'agnus_cunctipotens' : 'fgghhgfef.fghhj!hgfghh.hfgfeg.ghff.fh!j.!kj!jhgfghh.hfgfeg.ghf.fgghhgfef.fghhj!hgfghh.hfgfeg.ghff.', \
\
      'gloria_rex_splendens' : 'hghgffghhgghgff.fghhgfgddcdcff.fghhgfggf.hghghf.hhhgfgfd.ddcfgfd.hhhgfgfd.edccdcdfgf.ffghgffededdc.fghhfg.hgfggf.feghgfghhghgfef.h!hghgfddcfgff.hgfgfd.fghhhgff.fghhgff.ddcfggf.fghhfgfeed.fghhgfgf.ggfgghgfgghh.fghhhghfghggf.fgfghgfghggf.edefeed.fghhfgfgghh.fgfggh.fghgfgff.ghh!hh.fghhgfgdedcdff.ffggfghhgfggfe.d.dggfghg.f.', \
\
      'agnus_de_angelis' : 'fggfghf_g_f_f.ffddcdcdff_g_f_f.fghhg!hghf_g_f_f.fhjjhgjj.jhghfgfghf_g_f_f.fghhg!hghf_g_f_f.fggfghf_g_f_f.ffddcdcdff_g_f_f.fghhg!hghf_g_f_f.', \
\
      'kyrie_xvii' : 'fgfgh.j!hghfeghggf.fgfgh.j!hghfeghggf.fgfgh.j!hghfeghggf.jj.h!j.j!hghfeghggf.jj.h!j.j!hghfeghggf.jj.h!j.j!hghfeghggf.fhjjjk!j.j!hghfeghggf.fhjjjk!j.j!hghfeghggf.fhjjjk!j.fhjjk!j.j!hghfeghggf.', \
\
      'kyrie_firmator_sancte' : 'fdff.gh!hgffdef.fdff.gh!hgffdef.fdff.gh!hgffdef.fjj!h!jkjjh!hgffdef.fjj!h!jkjjh!hgffdef.fjj!h!jkjjh!hgffdef.fjjkjmlkj.!jkjjh!hgffdef.fjjkjmlkj.!jkjjh.j!jkjjh!hgffdef.', \
\
      'agnus_ad_lib_ii' : '!hghf.efggfdec.fdefg.f.!hghf.efggfdec.hfefg.f.!hghf.efggfdec.fdefg.f.', \
\
      'ant_crucifixus' : 'fghghf.ghgfdfefd_e_dcdd.c.dffgh_ghgf_dfefd_e_dcdd_c_fggff.', \
\
      'ant_gaudent_in_caelis' : 'ffgfedff_ffghghgf.f.ffdfg!!hghh_gfegghgf.f.fffcfh!j_j!!hgfgf!!hg_feghgf.f.fghhg!!hg.gfghhhghgf.f.', \
\
      'communio_exsultavit' : 'cdffd.dcfgfef.fhghjijhjff_g_f_f.ffhjjfgh_g_jijhjg.fhghgegefede.d.fff.hijji_h_fhghgf.ffgfffhjjhjgfedgeff.', \
\
      'resp_brev_hodie_scietis' : 'fgfffghh.g.fghgfdfggff.fgfffghh.g.fghgfdfggff.hh!hhghgg_hgfg_hh.g.fghgfdfggff.hhhh!h_hghgg_gghgfgg.h.fgfffghh.g.fghgfdfggff.', \
\
      'introit_hodie_scietis' : 'dfffffgg!hgg.f.fdddfg_gfffdcde_d_cdfffgff.dffgffef.dfefdedcdd_c_fffffgf.fggfghhhhg!hgf.fghhjg.fffffffgfdfgf.dfffffgg!hgg.f.fdddfg_gfffdcde_d_cdfffgff.dffgffef.dfefdedcdd_c_fffffgf.', \
\
      'ant_ipse_invocabit' : 'fffeggh_ffdc.fffeghh_hh_ggf.fghhhhghff.hhhfghgff.fghhhhg.hhhghf.hhfghgf.fffeggh_ffdc.fffeghh_hh_ggf.', \
\
      'ant_regina_caeli' : 'fgfghh.!hg!hfgf.hghfggff_!gfghf.fj_jkkj!hgfghh.!!!_g!jfgf.!!!_g!jfgf.ghghf_g_f_f.!hgfghfhgfeff.!jkjj!j_jfgf.!hg!j_jfgff.jjfgh!hgfegff.ffhjkjj!gh.j!hfgf.fhjkjj!gh.j!hfgf.g!hghf_g_f_f.', \
     }

def get_noise(x):
    return x * random.random() * random.choice([-1, 1])
     
def load_strings(s, order):
    table = {}
    for i in range(len(s) - order):
        try:
            table[s[i:i + order]]
        except KeyError:
            table[s[i:i + order]] = []
        table[s[i:i + order]] += s[i + order]
    return table

def generate(order, strings_to_load, start = None, max_length = 20):
    table = load_strings(strings_to_load, order)
    if start == None:
        s = random.choice(table.keys())
    else:
        s = start
    try:
        while len(s) < max_length:
            s += random.choice(table[s[-order:]])
    except KeyError:
        pass
    return s

# while starting_order >=0:
#     print 'Order', starting_order
#     print 'Output:'
#     #for i in range(5):
#     #    print generate(start='f_fg', max_length=100)
#     print generate(starting_order, ''.join(VI.values()), start='f_fg', max_length=80)
#     print ''
#     starting_order -= 1

print '##############################'

#take the output of the markov generator and makes a list of note-length tuples
def create_midi_list(markov):
    score = []
    for i in range(len(markov)):
        noise = get_noise(0.09) #this number will be added to each note length
                                #causing a bit of variation; it will be a float
                                #between itself and its negative, eg. -0.09 -- +0.09
        if markov[i] == '.' or markov[i] == '_':
            continue
        elif i == len(markov) - 1:
            score.append(( NOTES[markov[i]], round(0.6 + noise, 3) )) # if this is the last note
        elif markov[i+1] == '.': #if this note is followed by a '.'
            if markov[i-1] == '.': #if this is something like 'g.f.'
                if random.randrange(3) == 2: #there should be a chance of adding an extra long one
                    score[-1] = ( NOTES[markov[i-2]], round(1.6 * (1 + noise), 3) ) #both of the notes are made longer actually
                    score.append(( NOTES[markov[i]], round(2.0 * (1 + noise), 3) )) 
                    print 'LONG ONE!', markov[i-2] + markov[i-1] + markov[i] + markov[i+1] + markov[i+2] + markov[i+3]
                else:
                    score.append(( NOTES[markov[i]], round(1.5 * (1 + noise), 3) )) 
                score.append(( None, round(0.4 + get_noise(0.09), 3) )) #in either case add a delay for all 'g.f.'-likes
            elif i < len(markov) - 3 and markov[i+3] != '.': #just one '.' as in 'f.'
                if random.randrange(4) == 3:
                    score.append(( NOTES[markov[i]], round(1.8 * (1 + noise), 3) )) 
                else:
                    score.append(( NOTES[markov[i]], round(1.5 * (1 + noise), 3) )) 
                score.append(( None, round(0.3 + get_noise(0.09), 3) )) #a delay after 'f.'s too
        elif markov[i+1] == '_':
            score.append(( NOTES[markov[i]], round(0.8 + noise, 3) ))
        else:
            score.append(( NOTES[markov[i]], round(0.5 + noise, 3) ))
    return score

markov = generate(order=4, strings_to_load=''.join(VI.values()), max_length=400)
print markov
score = create_midi_list(markov)


player.note_on(54, 50, 1) #drone
player.note_on(61-12, 50, 1) #drone
speed = 0.8 #a multiplier: smaller means faster
for i in range(len(score)):
    if score[i][0]:
        player.note_on(score[i][0], 127, 1) #melody
        time.sleep(score[i][1]*speed)
        player.note_off(score[i][0], 127, 1)
    else:
        time.sleep(score[i][1]*speed)
        print 'REST!'
player.note_off(54, 50, 1) #drone
player.note_off(61, 50, 1) #drone
midi.quit()

raw_input('\n >')
