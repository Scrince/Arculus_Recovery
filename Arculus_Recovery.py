#!/usr/bin/env python3
"""
Standalone offline BIP39/BIP32 restore tool with optional Tkinter GUI.
No external dependencies (Python standard library only).
"""

import argparse
import base64
import csv
import hashlib
import hmac
import io
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Tuple


# --- Embedded BIP39 English word list ---
BIP39_WORDS = [
    'abandon',
    'ability',
    'able',
    'about',
    'above',
    'absent',
    'absorb',
    'abstract',
    'absurd',
    'abuse',
    'access',
    'accident',
    'account',
    'accuse',
    'achieve',
    'acid',
    'acoustic',
    'acquire',
    'across',
    'act',
    'action',
    'actor',
    'actress',
    'actual',
    'adapt',
    'add',
    'addict',
    'address',
    'adjust',
    'admit',
    'adult',
    'advance',
    'advice',
    'aerobic',
    'affair',
    'afford',
    'afraid',
    'again',
    'age',
    'agent',
    'agree',
    'ahead',
    'aim',
    'air',
    'airport',
    'aisle',
    'alarm',
    'album',
    'alcohol',
    'alert',
    'alien',
    'all',
    'alley',
    'allow',
    'almost',
    'alone',
    'alpha',
    'already',
    'also',
    'alter',
    'always',
    'amateur',
    'amazing',
    'among',
    'amount',
    'amused',
    'analyst',
    'anchor',
    'ancient',
    'anger',
    'angle',
    'angry',
    'animal',
    'ankle',
    'announce',
    'annual',
    'another',
    'answer',
    'antenna',
    'antique',
    'anxiety',
    'any',
    'apart',
    'apology',
    'appear',
    'apple',
    'approve',
    'april',
    'arch',
    'arctic',
    'area',
    'arena',
    'argue',
    'arm',
    'armed',
    'armor',
    'army',
    'around',
    'arrange',
    'arrest',
    'arrive',
    'arrow',
    'art',
    'artefact',
    'artist',
    'artwork',
    'ask',
    'aspect',
    'assault',
    'asset',
    'assist',
    'assume',
    'asthma',
    'athlete',
    'atom',
    'attack',
    'attend',
    'attitude',
    'attract',
    'auction',
    'audit',
    'august',
    'aunt',
    'author',
    'auto',
    'autumn',
    'average',
    'avocado',
    'avoid',
    'awake',
    'aware',
    'away',
    'awesome',
    'awful',
    'awkward',
    'axis',
    'baby',
    'bachelor',
    'bacon',
    'badge',
    'bag',
    'balance',
    'balcony',
    'ball',
    'bamboo',
    'banana',
    'banner',
    'bar',
    'barely',
    'bargain',
    'barrel',
    'base',
    'basic',
    'basket',
    'battle',
    'beach',
    'bean',
    'beauty',
    'because',
    'become',
    'beef',
    'before',
    'begin',
    'behave',
    'behind',
    'believe',
    'below',
    'belt',
    'bench',
    'benefit',
    'best',
    'betray',
    'better',
    'between',
    'beyond',
    'bicycle',
    'bid',
    'bike',
    'bind',
    'biology',
    'bird',
    'birth',
    'bitter',
    'black',
    'blade',
    'blame',
    'blanket',
    'blast',
    'bleak',
    'bless',
    'blind',
    'blood',
    'blossom',
    'blouse',
    'blue',
    'blur',
    'blush',
    'board',
    'boat',
    'body',
    'boil',
    'bomb',
    'bone',
    'bonus',
    'book',
    'boost',
    'border',
    'boring',
    'borrow',
    'boss',
    'bottom',
    'bounce',
    'box',
    'boy',
    'bracket',
    'brain',
    'brand',
    'brass',
    'brave',
    'bread',
    'breeze',
    'brick',
    'bridge',
    'brief',
    'bright',
    'bring',
    'brisk',
    'broccoli',
    'broken',
    'bronze',
    'broom',
    'brother',
    'brown',
    'brush',
    'bubble',
    'buddy',
    'budget',
    'buffalo',
    'build',
    'bulb',
    'bulk',
    'bullet',
    'bundle',
    'bunker',
    'burden',
    'burger',
    'burst',
    'bus',
    'business',
    'busy',
    'butter',
    'buyer',
    'buzz',
    'cabbage',
    'cabin',
    'cable',
    'cactus',
    'cage',
    'cake',
    'call',
    'calm',
    'camera',
    'camp',
    'can',
    'canal',
    'cancel',
    'candy',
    'cannon',
    'canoe',
    'canvas',
    'canyon',
    'capable',
    'capital',
    'captain',
    'car',
    'carbon',
    'card',
    'cargo',
    'carpet',
    'carry',
    'cart',
    'case',
    'cash',
    'casino',
    'castle',
    'casual',
    'cat',
    'catalog',
    'catch',
    'category',
    'cattle',
    'caught',
    'cause',
    'caution',
    'cave',
    'ceiling',
    'celery',
    'cement',
    'census',
    'century',
    'cereal',
    'certain',
    'chair',
    'chalk',
    'champion',
    'change',
    'chaos',
    'chapter',
    'charge',
    'chase',
    'chat',
    'cheap',
    'check',
    'cheese',
    'chef',
    'cherry',
    'chest',
    'chicken',
    'chief',
    'child',
    'chimney',
    'choice',
    'choose',
    'chronic',
    'chuckle',
    'chunk',
    'churn',
    'cigar',
    'cinnamon',
    'circle',
    'citizen',
    'city',
    'civil',
    'claim',
    'clap',
    'clarify',
    'claw',
    'clay',
    'clean',
    'clerk',
    'clever',
    'click',
    'client',
    'cliff',
    'climb',
    'clinic',
    'clip',
    'clock',
    'clog',
    'close',
    'cloth',
    'cloud',
    'clown',
    'club',
    'clump',
    'cluster',
    'clutch',
    'coach',
    'coast',
    'coconut',
    'code',
    'coffee',
    'coil',
    'coin',
    'collect',
    'color',
    'column',
    'combine',
    'come',
    'comfort',
    'comic',
    'common',
    'company',
    'concert',
    'conduct',
    'confirm',
    'congress',
    'connect',
    'consider',
    'control',
    'convince',
    'cook',
    'cool',
    'copper',
    'copy',
    'coral',
    'core',
    'corn',
    'correct',
    'cost',
    'cotton',
    'couch',
    'country',
    'couple',
    'course',
    'cousin',
    'cover',
    'coyote',
    'crack',
    'cradle',
    'craft',
    'cram',
    'crane',
    'crash',
    'crater',
    'crawl',
    'crazy',
    'cream',
    'credit',
    'creek',
    'crew',
    'cricket',
    'crime',
    'crisp',
    'critic',
    'crop',
    'cross',
    'crouch',
    'crowd',
    'crucial',
    'cruel',
    'cruise',
    'crumble',
    'crunch',
    'crush',
    'cry',
    'crystal',
    'cube',
    'culture',
    'cup',
    'cupboard',
    'curious',
    'current',
    'curtain',
    'curve',
    'cushion',
    'custom',
    'cute',
    'cycle',
    'dad',
    'damage',
    'damp',
    'dance',
    'danger',
    'daring',
    'dash',
    'daughter',
    'dawn',
    'day',
    'deal',
    'debate',
    'debris',
    'decade',
    'december',
    'decide',
    'decline',
    'decorate',
    'decrease',
    'deer',
    'defense',
    'define',
    'defy',
    'degree',
    'delay',
    'deliver',
    'demand',
    'demise',
    'denial',
    'dentist',
    'deny',
    'depart',
    'depend',
    'deposit',
    'depth',
    'deputy',
    'derive',
    'describe',
    'desert',
    'design',
    'desk',
    'despair',
    'destroy',
    'detail',
    'detect',
    'develop',
    'device',
    'devote',
    'diagram',
    'dial',
    'diamond',
    'diary',
    'dice',
    'diesel',
    'diet',
    'differ',
    'digital',
    'dignity',
    'dilemma',
    'dinner',
    'dinosaur',
    'direct',
    'dirt',
    'disagree',
    'discover',
    'disease',
    'dish',
    'dismiss',
    'disorder',
    'display',
    'distance',
    'divert',
    'divide',
    'divorce',
    'dizzy',
    'doctor',
    'document',
    'dog',
    'doll',
    'dolphin',
    'domain',
    'donate',
    'donkey',
    'donor',
    'door',
    'dose',
    'double',
    'dove',
    'draft',
    'dragon',
    'drama',
    'drastic',
    'draw',
    'dream',
    'dress',
    'drift',
    'drill',
    'drink',
    'drip',
    'drive',
    'drop',
    'drum',
    'dry',
    'duck',
    'dumb',
    'dune',
    'during',
    'dust',
    'dutch',
    'duty',
    'dwarf',
    'dynamic',
    'eager',
    'eagle',
    'early',
    'earn',
    'earth',
    'easily',
    'east',
    'easy',
    'echo',
    'ecology',
    'economy',
    'edge',
    'edit',
    'educate',
    'effort',
    'egg',
    'eight',
    'either',
    'elbow',
    'elder',
    'electric',
    'elegant',
    'element',
    'elephant',
    'elevator',
    'elite',
    'else',
    'embark',
    'embody',
    'embrace',
    'emerge',
    'emotion',
    'employ',
    'empower',
    'empty',
    'enable',
    'enact',
    'end',
    'endless',
    'endorse',
    'enemy',
    'energy',
    'enforce',
    'engage',
    'engine',
    'enhance',
    'enjoy',
    'enlist',
    'enough',
    'enrich',
    'enroll',
    'ensure',
    'enter',
    'entire',
    'entry',
    'envelope',
    'episode',
    'equal',
    'equip',
    'era',
    'erase',
    'erode',
    'erosion',
    'error',
    'erupt',
    'escape',
    'essay',
    'essence',
    'estate',
    'eternal',
    'ethics',
    'evidence',
    'evil',
    'evoke',
    'evolve',
    'exact',
    'example',
    'excess',
    'exchange',
    'excite',
    'exclude',
    'excuse',
    'execute',
    'exercise',
    'exhaust',
    'exhibit',
    'exile',
    'exist',
    'exit',
    'exotic',
    'expand',
    'expect',
    'expire',
    'explain',
    'expose',
    'express',
    'extend',
    'extra',
    'eye',
    'eyebrow',
    'fabric',
    'face',
    'faculty',
    'fade',
    'faint',
    'faith',
    'fall',
    'false',
    'fame',
    'family',
    'famous',
    'fan',
    'fancy',
    'fantasy',
    'farm',
    'fashion',
    'fat',
    'fatal',
    'father',
    'fatigue',
    'fault',
    'favorite',
    'feature',
    'february',
    'federal',
    'fee',
    'feed',
    'feel',
    'female',
    'fence',
    'festival',
    'fetch',
    'fever',
    'few',
    'fiber',
    'fiction',
    'field',
    'figure',
    'file',
    'film',
    'filter',
    'final',
    'find',
    'fine',
    'finger',
    'finish',
    'fire',
    'firm',
    'first',
    'fiscal',
    'fish',
    'fit',
    'fitness',
    'fix',
    'flag',
    'flame',
    'flash',
    'flat',
    'flavor',
    'flee',
    'flight',
    'flip',
    'float',
    'flock',
    'floor',
    'flower',
    'fluid',
    'flush',
    'fly',
    'foam',
    'focus',
    'fog',
    'foil',
    'fold',
    'follow',
    'food',
    'foot',
    'force',
    'forest',
    'forget',
    'fork',
    'fortune',
    'forum',
    'forward',
    'fossil',
    'foster',
    'found',
    'fox',
    'fragile',
    'frame',
    'frequent',
    'fresh',
    'friend',
    'fringe',
    'frog',
    'front',
    'frost',
    'frown',
    'frozen',
    'fruit',
    'fuel',
    'fun',
    'funny',
    'furnace',
    'fury',
    'future',
    'gadget',
    'gain',
    'galaxy',
    'gallery',
    'game',
    'gap',
    'garage',
    'garbage',
    'garden',
    'garlic',
    'garment',
    'gas',
    'gasp',
    'gate',
    'gather',
    'gauge',
    'gaze',
    'general',
    'genius',
    'genre',
    'gentle',
    'genuine',
    'gesture',
    'ghost',
    'giant',
    'gift',
    'giggle',
    'ginger',
    'giraffe',
    'girl',
    'give',
    'glad',
    'glance',
    'glare',
    'glass',
    'glide',
    'glimpse',
    'globe',
    'gloom',
    'glory',
    'glove',
    'glow',
    'glue',
    'goat',
    'goddess',
    'gold',
    'good',
    'goose',
    'gorilla',
    'gospel',
    'gossip',
    'govern',
    'gown',
    'grab',
    'grace',
    'grain',
    'grant',
    'grape',
    'grass',
    'gravity',
    'great',
    'green',
    'grid',
    'grief',
    'grit',
    'grocery',
    'group',
    'grow',
    'grunt',
    'guard',
    'guess',
    'guide',
    'guilt',
    'guitar',
    'gun',
    'gym',
    'habit',
    'hair',
    'half',
    'hammer',
    'hamster',
    'hand',
    'happy',
    'harbor',
    'hard',
    'harsh',
    'harvest',
    'hat',
    'have',
    'hawk',
    'hazard',
    'head',
    'health',
    'heart',
    'heavy',
    'hedgehog',
    'height',
    'hello',
    'helmet',
    'help',
    'hen',
    'hero',
    'hidden',
    'high',
    'hill',
    'hint',
    'hip',
    'hire',
    'history',
    'hobby',
    'hockey',
    'hold',
    'hole',
    'holiday',
    'hollow',
    'home',
    'honey',
    'hood',
    'hope',
    'horn',
    'horror',
    'horse',
    'hospital',
    'host',
    'hotel',
    'hour',
    'hover',
    'hub',
    'huge',
    'human',
    'humble',
    'humor',
    'hundred',
    'hungry',
    'hunt',
    'hurdle',
    'hurry',
    'hurt',
    'husband',
    'hybrid',
    'ice',
    'icon',
    'idea',
    'identify',
    'idle',
    'ignore',
    'ill',
    'illegal',
    'illness',
    'image',
    'imitate',
    'immense',
    'immune',
    'impact',
    'impose',
    'improve',
    'impulse',
    'inch',
    'include',
    'income',
    'increase',
    'index',
    'indicate',
    'indoor',
    'industry',
    'infant',
    'inflict',
    'inform',
    'inhale',
    'inherit',
    'initial',
    'inject',
    'injury',
    'inmate',
    'inner',
    'innocent',
    'input',
    'inquiry',
    'insane',
    'insect',
    'inside',
    'inspire',
    'install',
    'intact',
    'interest',
    'into',
    'invest',
    'invite',
    'involve',
    'iron',
    'island',
    'isolate',
    'issue',
    'item',
    'ivory',
    'jacket',
    'jaguar',
    'jar',
    'jazz',
    'jealous',
    'jeans',
    'jelly',
    'jewel',
    'job',
    'join',
    'joke',
    'journey',
    'joy',
    'judge',
    'juice',
    'jump',
    'jungle',
    'junior',
    'junk',
    'just',
    'kangaroo',
    'keen',
    'keep',
    'ketchup',
    'key',
    'kick',
    'kid',
    'kidney',
    'kind',
    'kingdom',
    'kiss',
    'kit',
    'kitchen',
    'kite',
    'kitten',
    'kiwi',
    'knee',
    'knife',
    'knock',
    'know',
    'lab',
    'label',
    'labor',
    'ladder',
    'lady',
    'lake',
    'lamp',
    'language',
    'laptop',
    'large',
    'later',
    'latin',
    'laugh',
    'laundry',
    'lava',
    'law',
    'lawn',
    'lawsuit',
    'layer',
    'lazy',
    'leader',
    'leaf',
    'learn',
    'leave',
    'lecture',
    'left',
    'leg',
    'legal',
    'legend',
    'leisure',
    'lemon',
    'lend',
    'length',
    'lens',
    'leopard',
    'lesson',
    'letter',
    'level',
    'liar',
    'liberty',
    'library',
    'license',
    'life',
    'lift',
    'light',
    'like',
    'limb',
    'limit',
    'link',
    'lion',
    'liquid',
    'list',
    'little',
    'live',
    'lizard',
    'load',
    'loan',
    'lobster',
    'local',
    'lock',
    'logic',
    'lonely',
    'long',
    'loop',
    'lottery',
    'loud',
    'lounge',
    'love',
    'loyal',
    'lucky',
    'luggage',
    'lumber',
    'lunar',
    'lunch',
    'luxury',
    'lyrics',
    'machine',
    'mad',
    'magic',
    'magnet',
    'maid',
    'mail',
    'main',
    'major',
    'make',
    'mammal',
    'man',
    'manage',
    'mandate',
    'mango',
    'mansion',
    'manual',
    'maple',
    'marble',
    'march',
    'margin',
    'marine',
    'market',
    'marriage',
    'mask',
    'mass',
    'master',
    'match',
    'material',
    'math',
    'matrix',
    'matter',
    'maximum',
    'maze',
    'meadow',
    'mean',
    'measure',
    'meat',
    'mechanic',
    'medal',
    'media',
    'melody',
    'melt',
    'member',
    'memory',
    'mention',
    'menu',
    'mercy',
    'merge',
    'merit',
    'merry',
    'mesh',
    'message',
    'metal',
    'method',
    'middle',
    'midnight',
    'milk',
    'million',
    'mimic',
    'mind',
    'minimum',
    'minor',
    'minute',
    'miracle',
    'mirror',
    'misery',
    'miss',
    'mistake',
    'mix',
    'mixed',
    'mixture',
    'mobile',
    'model',
    'modify',
    'mom',
    'moment',
    'monitor',
    'monkey',
    'monster',
    'month',
    'moon',
    'moral',
    'more',
    'morning',
    'mosquito',
    'mother',
    'motion',
    'motor',
    'mountain',
    'mouse',
    'move',
    'movie',
    'much',
    'muffin',
    'mule',
    'multiply',
    'muscle',
    'museum',
    'mushroom',
    'music',
    'must',
    'mutual',
    'myself',
    'mystery',
    'myth',
    'naive',
    'name',
    'napkin',
    'narrow',
    'nasty',
    'nation',
    'nature',
    'near',
    'neck',
    'need',
    'negative',
    'neglect',
    'neither',
    'nephew',
    'nerve',
    'nest',
    'net',
    'network',
    'neutral',
    'never',
    'news',
    'next',
    'nice',
    'night',
    'noble',
    'noise',
    'nominee',
    'noodle',
    'normal',
    'north',
    'nose',
    'notable',
    'note',
    'nothing',
    'notice',
    'novel',
    'now',
    'nuclear',
    'number',
    'nurse',
    'nut',
    'oak',
    'obey',
    'object',
    'oblige',
    'obscure',
    'observe',
    'obtain',
    'obvious',
    'occur',
    'ocean',
    'october',
    'odor',
    'off',
    'offer',
    'office',
    'often',
    'oil',
    'okay',
    'old',
    'olive',
    'olympic',
    'omit',
    'once',
    'one',
    'onion',
    'online',
    'only',
    'open',
    'opera',
    'opinion',
    'oppose',
    'option',
    'orange',
    'orbit',
    'orchard',
    'order',
    'ordinary',
    'organ',
    'orient',
    'original',
    'orphan',
    'ostrich',
    'other',
    'outdoor',
    'outer',
    'output',
    'outside',
    'oval',
    'oven',
    'over',
    'own',
    'owner',
    'oxygen',
    'oyster',
    'ozone',
    'pact',
    'paddle',
    'page',
    'pair',
    'palace',
    'palm',
    'panda',
    'panel',
    'panic',
    'panther',
    'paper',
    'parade',
    'parent',
    'park',
    'parrot',
    'party',
    'pass',
    'patch',
    'path',
    'patient',
    'patrol',
    'pattern',
    'pause',
    'pave',
    'payment',
    'peace',
    'peanut',
    'pear',
    'peasant',
    'pelican',
    'pen',
    'penalty',
    'pencil',
    'people',
    'pepper',
    'perfect',
    'permit',
    'person',
    'pet',
    'phone',
    'photo',
    'phrase',
    'physical',
    'piano',
    'picnic',
    'picture',
    'piece',
    'pig',
    'pigeon',
    'pill',
    'pilot',
    'pink',
    'pioneer',
    'pipe',
    'pistol',
    'pitch',
    'pizza',
    'place',
    'planet',
    'plastic',
    'plate',
    'play',
    'please',
    'pledge',
    'pluck',
    'plug',
    'plunge',
    'poem',
    'poet',
    'point',
    'polar',
    'pole',
    'police',
    'pond',
    'pony',
    'pool',
    'popular',
    'portion',
    'position',
    'possible',
    'post',
    'potato',
    'pottery',
    'poverty',
    'powder',
    'power',
    'practice',
    'praise',
    'predict',
    'prefer',
    'prepare',
    'present',
    'pretty',
    'prevent',
    'price',
    'pride',
    'primary',
    'print',
    'priority',
    'prison',
    'private',
    'prize',
    'problem',
    'process',
    'produce',
    'profit',
    'program',
    'project',
    'promote',
    'proof',
    'property',
    'prosper',
    'protect',
    'proud',
    'provide',
    'public',
    'pudding',
    'pull',
    'pulp',
    'pulse',
    'pumpkin',
    'punch',
    'pupil',
    'puppy',
    'purchase',
    'purity',
    'purpose',
    'purse',
    'push',
    'put',
    'puzzle',
    'pyramid',
    'quality',
    'quantum',
    'quarter',
    'question',
    'quick',
    'quit',
    'quiz',
    'quote',
    'rabbit',
    'raccoon',
    'race',
    'rack',
    'radar',
    'radio',
    'rail',
    'rain',
    'raise',
    'rally',
    'ramp',
    'ranch',
    'random',
    'range',
    'rapid',
    'rare',
    'rate',
    'rather',
    'raven',
    'raw',
    'razor',
    'ready',
    'real',
    'reason',
    'rebel',
    'rebuild',
    'recall',
    'receive',
    'recipe',
    'record',
    'recycle',
    'reduce',
    'reflect',
    'reform',
    'refuse',
    'region',
    'regret',
    'regular',
    'reject',
    'relax',
    'release',
    'relief',
    'rely',
    'remain',
    'remember',
    'remind',
    'remove',
    'render',
    'renew',
    'rent',
    'reopen',
    'repair',
    'repeat',
    'replace',
    'report',
    'require',
    'rescue',
    'resemble',
    'resist',
    'resource',
    'response',
    'result',
    'retire',
    'retreat',
    'return',
    'reunion',
    'reveal',
    'review',
    'reward',
    'rhythm',
    'rib',
    'ribbon',
    'rice',
    'rich',
    'ride',
    'ridge',
    'rifle',
    'right',
    'rigid',
    'ring',
    'riot',
    'ripple',
    'risk',
    'ritual',
    'rival',
    'river',
    'road',
    'roast',
    'robot',
    'robust',
    'rocket',
    'romance',
    'roof',
    'rookie',
    'room',
    'rose',
    'rotate',
    'rough',
    'round',
    'route',
    'royal',
    'rubber',
    'rude',
    'rug',
    'rule',
    'run',
    'runway',
    'rural',
    'sad',
    'saddle',
    'sadness',
    'safe',
    'sail',
    'salad',
    'salmon',
    'salon',
    'salt',
    'salute',
    'same',
    'sample',
    'sand',
    'satisfy',
    'satoshi',
    'sauce',
    'sausage',
    'save',
    'say',
    'scale',
    'scan',
    'scare',
    'scatter',
    'scene',
    'scheme',
    'school',
    'science',
    'scissors',
    'scorpion',
    'scout',
    'scrap',
    'screen',
    'script',
    'scrub',
    'sea',
    'search',
    'season',
    'seat',
    'second',
    'secret',
    'section',
    'security',
    'seed',
    'seek',
    'segment',
    'select',
    'sell',
    'seminar',
    'senior',
    'sense',
    'sentence',
    'series',
    'service',
    'session',
    'settle',
    'setup',
    'seven',
    'shadow',
    'shaft',
    'shallow',
    'share',
    'shed',
    'shell',
    'sheriff',
    'shield',
    'shift',
    'shine',
    'ship',
    'shiver',
    'shock',
    'shoe',
    'shoot',
    'shop',
    'short',
    'shoulder',
    'shove',
    'shrimp',
    'shrug',
    'shuffle',
    'shy',
    'sibling',
    'sick',
    'side',
    'siege',
    'sight',
    'sign',
    'silent',
    'silk',
    'silly',
    'silver',
    'similar',
    'simple',
    'since',
    'sing',
    'siren',
    'sister',
    'situate',
    'six',
    'size',
    'skate',
    'sketch',
    'ski',
    'skill',
    'skin',
    'skirt',
    'skull',
    'slab',
    'slam',
    'sleep',
    'slender',
    'slice',
    'slide',
    'slight',
    'slim',
    'slogan',
    'slot',
    'slow',
    'slush',
    'small',
    'smart',
    'smile',
    'smoke',
    'smooth',
    'snack',
    'snake',
    'snap',
    'sniff',
    'snow',
    'soap',
    'soccer',
    'social',
    'sock',
    'soda',
    'soft',
    'solar',
    'soldier',
    'solid',
    'solution',
    'solve',
    'someone',
    'song',
    'soon',
    'sorry',
    'sort',
    'soul',
    'sound',
    'soup',
    'source',
    'south',
    'space',
    'spare',
    'spatial',
    'spawn',
    'speak',
    'special',
    'speed',
    'spell',
    'spend',
    'sphere',
    'spice',
    'spider',
    'spike',
    'spin',
    'spirit',
    'split',
    'spoil',
    'sponsor',
    'spoon',
    'sport',
    'spot',
    'spray',
    'spread',
    'spring',
    'spy',
    'square',
    'squeeze',
    'squirrel',
    'stable',
    'stadium',
    'staff',
    'stage',
    'stairs',
    'stamp',
    'stand',
    'start',
    'state',
    'stay',
    'steak',
    'steel',
    'stem',
    'step',
    'stereo',
    'stick',
    'still',
    'sting',
    'stock',
    'stomach',
    'stone',
    'stool',
    'story',
    'stove',
    'strategy',
    'street',
    'strike',
    'strong',
    'struggle',
    'student',
    'stuff',
    'stumble',
    'style',
    'subject',
    'submit',
    'subway',
    'success',
    'such',
    'sudden',
    'suffer',
    'sugar',
    'suggest',
    'suit',
    'summer',
    'sun',
    'sunny',
    'sunset',
    'super',
    'supply',
    'supreme',
    'sure',
    'surface',
    'surge',
    'surprise',
    'surround',
    'survey',
    'suspect',
    'sustain',
    'swallow',
    'swamp',
    'swap',
    'swarm',
    'swear',
    'sweet',
    'swift',
    'swim',
    'swing',
    'switch',
    'sword',
    'symbol',
    'symptom',
    'syrup',
    'system',
    'table',
    'tackle',
    'tag',
    'tail',
    'talent',
    'talk',
    'tank',
    'tape',
    'target',
    'task',
    'taste',
    'tattoo',
    'taxi',
    'teach',
    'team',
    'tell',
    'ten',
    'tenant',
    'tennis',
    'tent',
    'term',
    'test',
    'text',
    'thank',
    'that',
    'theme',
    'then',
    'theory',
    'there',
    'they',
    'thing',
    'this',
    'thought',
    'three',
    'thrive',
    'throw',
    'thumb',
    'thunder',
    'ticket',
    'tide',
    'tiger',
    'tilt',
    'timber',
    'time',
    'tiny',
    'tip',
    'tired',
    'tissue',
    'title',
    'toast',
    'tobacco',
    'today',
    'toddler',
    'toe',
    'together',
    'toilet',
    'token',
    'tomato',
    'tomorrow',
    'tone',
    'tongue',
    'tonight',
    'tool',
    'tooth',
    'top',
    'topic',
    'topple',
    'torch',
    'tornado',
    'tortoise',
    'toss',
    'total',
    'tourist',
    'toward',
    'tower',
    'town',
    'toy',
    'track',
    'trade',
    'traffic',
    'tragic',
    'train',
    'transfer',
    'trap',
    'trash',
    'travel',
    'tray',
    'treat',
    'tree',
    'trend',
    'trial',
    'tribe',
    'trick',
    'trigger',
    'trim',
    'trip',
    'trophy',
    'trouble',
    'truck',
    'true',
    'truly',
    'trumpet',
    'trust',
    'truth',
    'try',
    'tube',
    'tuition',
    'tumble',
    'tuna',
    'tunnel',
    'turkey',
    'turn',
    'turtle',
    'twelve',
    'twenty',
    'twice',
    'twin',
    'twist',
    'two',
    'type',
    'typical',
    'ugly',
    'umbrella',
    'unable',
    'unaware',
    'uncle',
    'uncover',
    'under',
    'undo',
    'unfair',
    'unfold',
    'unhappy',
    'uniform',
    'unique',
    'unit',
    'universe',
    'unknown',
    'unlock',
    'until',
    'unusual',
    'unveil',
    'update',
    'upgrade',
    'uphold',
    'upon',
    'upper',
    'upset',
    'urban',
    'urge',
    'usage',
    'use',
    'used',
    'useful',
    'useless',
    'usual',
    'utility',
    'vacant',
    'vacuum',
    'vague',
    'valid',
    'valley',
    'valve',
    'van',
    'vanish',
    'vapor',
    'various',
    'vast',
    'vault',
    'vehicle',
    'velvet',
    'vendor',
    'venture',
    'venue',
    'verb',
    'verify',
    'version',
    'very',
    'vessel',
    'veteran',
    'viable',
    'vibrant',
    'vicious',
    'victory',
    'video',
    'view',
    'village',
    'vintage',
    'violin',
    'virtual',
    'virus',
    'visa',
    'visit',
    'visual',
    'vital',
    'vivid',
    'vocal',
    'voice',
    'void',
    'volcano',
    'volume',
    'vote',
    'voyage',
    'wage',
    'wagon',
    'wait',
    'walk',
    'wall',
    'walnut',
    'want',
    'warfare',
    'warm',
    'warrior',
    'wash',
    'wasp',
    'waste',
    'water',
    'wave',
    'way',
    'wealth',
    'weapon',
    'wear',
    'weasel',
    'weather',
    'web',
    'wedding',
    'weekend',
    'weird',
    'welcome',
    'west',
    'wet',
    'whale',
    'what',
    'wheat',
    'wheel',
    'when',
    'where',
    'whip',
    'whisper',
    'wide',
    'width',
    'wife',
    'wild',
    'will',
    'win',
    'window',
    'wine',
    'wing',
    'wink',
    'winner',
    'winter',
    'wire',
    'wisdom',
    'wise',
    'wish',
    'witness',
    'wolf',
    'woman',
    'wonder',
    'wood',
    'wool',
    'word',
    'work',
    'world',
    'worry',
    'worth',
    'wrap',
    'wreck',
    'wrestle',
    'wrist',
    'write',
    'wrong',
    'yard',
    'year',
    'yellow',
    'you',
    'young',
    'youth',
    'zebra',
    'zero',
    'zone',
    'zoo',
]
BIP39_WORD_INDEX = {w: i for i, w in enumerate(BIP39_WORDS)}


# secp256k1 domain params
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)

HARDENED = 0x80000000

BTC_MAINNET = {
    "p2pkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2wpkh-p2sh": {"xprv": 0x049D7878, "xpub": 0x049D7CB2},
    "p2wpkh": {"xprv": 0x04B2430C, "xpub": 0x04B24746},
    "p2tr": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "wif": 0x80,
    "p2pkh_prefix": 0x00,
    "p2sh_prefix": 0x05,
    "hrp": "bc",
}

BTC_TESTNET = {
    "p2pkh": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "p2wpkh-p2sh": {"xprv": 0x044A4E28, "xpub": 0x044A5262},
    "p2wpkh": {"xprv": 0x045F18BC, "xpub": 0x045F1CF6},
    "p2tr": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "wif": 0xEF,
    "p2pkh_prefix": 0x6F,
    "p2sh_prefix": 0xC4,
    "hrp": "tb",
}

LTC_MAINNET = {
    # SLIP-0132 versions for Litecoin where applicable.
    "p2pkh": {"xprv": 0x019D9CFE, "xpub": 0x019DA462},
    "p2wpkh-p2sh": {"xprv": 0x01B26792, "xpub": 0x01B26EF6},
    # Keep native-segwit extended versions aligned with existing output format.
    "p2wpkh": {"xprv": 0x04B2430C, "xpub": 0x04B24746},
    "p2tr": {"xprv": 0x019D9CFE, "xpub": 0x019DA462},
    "wif": 0xB0,
    "p2pkh_prefix": 0x30,
    "p2sh_prefix": 0x32,
    "hrp": "ltc",
}

DOGE_MAINNET = {
    # Dogecoin mainnet BIP32 version bytes (dgpv/dgub).
    "p2pkh": {"xprv": 0x02FAC398, "xpub": 0x02FACAFD},
    # Dogecoin does not have widely adopted SLIP-0132 y/z versions.
    # Reuse Dogecoin BIP32 versions so extended keys remain consistent.
    "p2wpkh-p2sh": {"xprv": 0x02FAC398, "xpub": 0x02FACAFD},
    "p2wpkh": {"xprv": 0x02FAC398, "xpub": 0x02FACAFD},
    "p2tr": None,
    "wif": 0x9E,
    "p2pkh_prefix": 0x1E,
    "p2sh_prefix": 0x16,
    "hrp": "doge",
}

COINS = {
    "bitcoin": {"coin_type": 0, "mainnet": BTC_MAINNET, "testnet": BTC_TESTNET},
    "litecoin": {"coin_type": 2, "mainnet": LTC_MAINNET, "testnet": None},
    "dogecoin": {"coin_type": 3, "mainnet": DOGE_MAINNET, "testnet": None},
}

DEFAULT_ACCOUNT_DERIVATION = {
    "bitcoin": "m/0'",
    "litecoin": "m/84'/2'/0'",
    "dogecoin": "m/44'/3'/0'",
}

B58_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BECH32_ALPHABET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def hash160(b: bytes) -> bytes:
    h = hashlib.new("ripemd160")
    h.update(hashlib.sha256(b).digest())
    return h.digest()


def hmac_sha512(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha512).digest()


def b58encode(raw: bytes) -> str:
    n = int.from_bytes(raw, "big")
    out = bytearray()
    while n > 0:
        n, r = divmod(n, 58)
        out.append(B58_ALPHABET[r])
    out.reverse()
    pad = 0
    for c in raw:
        if c == 0:
            pad += 1
        else:
            break
    return (B58_ALPHABET[0:1] * pad + out).decode("ascii")


def b58check(payload: bytes) -> str:
    checksum = sha256(sha256(payload))[:4]
    return b58encode(payload + checksum)


def bech32_polymod(values: List[int]) -> int:
    gen = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = ((chk & 0x1FFFFFF) << 5) ^ v
        for i in range(5):
            if (top >> i) & 1:
                chk ^= gen[i]
    return chk


def bech32_hrp_expand(hrp: str) -> List[int]:
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_create_checksum(hrp: str, data: List[int]) -> List[int]:
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> (5 * (5 - i))) & 31 for i in range(6)]


def bech32_encode(hrp: str, data: List[int]) -> str:
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + "1" + "".join(BECH32_ALPHABET[d] for d in combined)


def bech32m_create_checksum(hrp: str, data: List[int]) -> List[int]:
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 0x2BC830A3
    return [(polymod >> (5 * (5 - i))) & 31 for i in range(6)]


def bech32m_encode(hrp: str, data: List[int]) -> str:
    combined = data + bech32m_create_checksum(hrp, data)
    return hrp + "1" + "".join(BECH32_ALPHABET[d] for d in combined)


def convertbits(data: bytes, frombits: int, tobits: int, pad: bool = True) -> List[int]:
    acc = 0
    bits = 0
    out = []
    maxv = (1 << tobits) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            raise ValueError("invalid bits")
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            out.append((acc >> bits) & maxv)
    if pad:
        if bits:
            out.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        raise ValueError("invalid bits")
    return out


def segwit_addr_v0(hrp: str, witprog: bytes) -> str:
    return bech32_encode(hrp, [0] + convertbits(witprog, 8, 5))


def segwit_addr_v1(hrp: str, witprog: bytes) -> str:
    return bech32m_encode(hrp, [1] + convertbits(witprog, 8, 5))


def inv_mod(a: int, n: int) -> int:
    return pow(a, -1, n)


def point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p1 == p2:
        lam = (3 * x1 * x1) * inv_mod(2 * y1 % P, P) % P
    else:
        lam = (y2 - y1) * inv_mod((x2 - x1) % P, P) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)


def point_mul(k: int, point=G):
    if k % N == 0 or point is None:
        return None
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


def ser32(i: int) -> bytes:
    return i.to_bytes(4, "big")


def ser256(i: int) -> bytes:
    return i.to_bytes(32, "big")


def ser_pubkey(p) -> bytes:
    x, y = p
    return (b"\x03" if (y & 1) else b"\x02") + x.to_bytes(32, "big")


def xonly_pubkey(p) -> bytes:
    x, _ = p
    return x.to_bytes(32, "big")


def negate_point(p):
    if p is None:
        return None
    x, y = p
    return (x, (-y) % P)


def tagged_hash(tag: str, msg: bytes) -> bytes:
    tag_hash = sha256(tag.encode("utf-8"))
    return sha256(tag_hash + tag_hash + msg)


def normalize_nfkd(s: str) -> str:
    return unicodedata.normalize("NFKD", s)


def normalize_mnemonic_words(mnemonic: str) -> List[str]:
    return normalize_nfkd(" ".join(mnemonic.strip().split())).split(" ")


def bip39_validate(mnemonic: str) -> Tuple[bool, bool, str]:
    words = normalize_mnemonic_words(mnemonic)
    wc = len(words)
    if wc not in (12, 24):
        return False, False, "Only 12-word and 24-word mnemonics are supported."
    if any(w not in BIP39_WORD_INDEX for w in words):
        return False, False, "Mnemonic contains unknown words outside the BIP39 English list."

    acc = 0
    for w in words:
        acc = (acc << 11) | BIP39_WORD_INDEX[w]

    checksum_bits = wc // 3
    entropy_bits = wc * 11 - checksum_bits
    entropy_int = acc >> checksum_bits
    checksum_int = acc & ((1 << checksum_bits) - 1)

    entropy = entropy_int.to_bytes(entropy_bits // 8, "big")
    hash_int = int.from_bytes(sha256(entropy), "big")
    expected_checksum = hash_int >> (256 - checksum_bits)
    checksum_ok = checksum_int == expected_checksum
    if not checksum_ok:
        return True, False, "Mnemonic words are valid BIP39 words, but checksum is invalid."
    return True, True, "Mnemonic is valid BIP39 (English word list + checksum)."


def generate_random_mnemonic(word_count: int) -> str:
    if word_count not in (12, 24):
        raise ValueError("Only 12-word and 24-word mnemonics are supported.")
    checksum_bits = word_count // 3
    entropy_bits = word_count * 11 - checksum_bits
    entropy = os.urandom(entropy_bits // 8)
    checksum = int.from_bytes(sha256(entropy), "big") >> (256 - checksum_bits)
    bits = (int.from_bytes(entropy, "big") << checksum_bits) | checksum
    words = [None] * word_count
    for i in range(word_count - 1, -1, -1):
        words[i] = BIP39_WORDS[bits & 0x7FF]
        bits >>= 11
    mnemonic = " ".join(words)
    words_ok, checksum_ok, _ = bip39_validate(mnemonic)
    if not (words_ok and checksum_ok):
        raise ValueError("Generated mnemonic failed validation.")
    return mnemonic


def detect_seed_format(word_count: int, words_ok: bool, checksum_ok: bool) -> Tuple[str, str]:
    if word_count in (12, 24) and words_ok and checksum_ok:
        return "HD wallet mnemonic", "BIP-39 mnemonic (English)"
    if word_count in (12, 24) and words_ok:
        return "Unrecognized or incomplete wallet seed", "BIP-39-like mnemonic (English words, checksum invalid)"
    return "Unknown", "Unknown or unsupported mnemonic format"


def analyze_mnemonic(mnemonic: str, passphrase: str = "") -> Dict:
    words = normalize_mnemonic_words(mnemonic)
    wc = len(words)
    details = {
        "word_count": wc,
        "wordlist_validity": "Invalid",
        "entropy_bits": None,
        "checksum_bits": None,
        "checksum_match": "Invalid",
        "bip39_compliance": "No",
        "bip39_seed_512_bit": None,
        "master_private_key": None,
        "master_chain_code": None,
        "root_fingerprint": None,
        "keystore_type": "Unknown",
        "seed_format_detection": "Unknown or unsupported mnemonic format",
        "passphrase_warning": None,
        "message": "",
    }
    if wc not in (12, 24):
        details["message"] = "Only 12-word and 24-word mnemonics are supported."
        return {"words_ok": False, "checksum_ok": False, **details}
    details["checksum_bits"] = wc // 3
    details["entropy_bits"] = wc * 11 - details["checksum_bits"]
    if any(w not in BIP39_WORD_INDEX for w in words):
        details["message"] = "Mnemonic contains unknown words outside the BIP39 English list."
        return {"words_ok": False, "checksum_ok": False, **details}

    details["wordlist_validity"] = "Valid"
    acc = 0
    for w in words:
        acc = (acc << 11) | BIP39_WORD_INDEX[w]
    checksum_bits = details["checksum_bits"]
    entropy_bits = details["entropy_bits"]
    entropy_int = acc >> checksum_bits
    checksum_int = acc & ((1 << checksum_bits) - 1)
    entropy = entropy_int.to_bytes(entropy_bits // 8, "big")
    hash_int = int.from_bytes(sha256(entropy), "big")
    expected_checksum = hash_int >> (256 - checksum_bits)
    checksum_ok = checksum_int == expected_checksum
    keystore_type, seed_format_detection = detect_seed_format(wc, True, checksum_ok)
    details["checksum_match"] = "Valid" if checksum_ok else "Invalid"
    details["bip39_compliance"] = "Yes" if checksum_ok else "No"
    details["keystore_type"] = keystore_type
    details["seed_format_detection"] = seed_format_detection
    details["passphrase_warning"] = "This seed may require a passphrase" if checksum_ok and not passphrase else None

    if not checksum_ok:
        details["message"] = "Mnemonic words are valid BIP39 words, but checksum is invalid."
        return {"words_ok": True, "checksum_ok": False, **details}

    seed = bip39_to_seed(mnemonic, passphrase)
    root = master_from_seed(seed)
    details["bip39_seed_512_bit"] = seed.hex()
    details["master_private_key"] = ser256(root.k).hex()
    details["master_chain_code"] = root.c.hex()
    details["root_fingerprint"] = hash160(ser_pubkey(root.pub()))[:4].hex()
    details["message"] = "Mnemonic is valid BIP39 (English word list + checksum)."
    return {"words_ok": True, "checksum_ok": True, **details}


def bip39_to_seed(mnemonic: str, passphrase: str) -> bytes:
    m = normalize_nfkd(" ".join(mnemonic.strip().split()))
    p = normalize_nfkd(passphrase)
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048, dklen=64)


def xor_stream_crypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < len(data):
        block = hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        out.extend(block)
        counter += 1
    return bytes(a ^ b for a, b in zip(data, out[: len(data)]))


ARC_MAGIC = "ARCULUS-ARC"
ARC_ARMOR_HEADER = "ARCULUS-ARC-V2"
ARC_V2_FORMAT = "arculus-encrypted-seed-v2"
ARC_V2_KDF_ITERATIONS = 1000000
ARC_V2_MIN_KDF_ITERATIONS = 600000
ARC_V2_SALT_BYTES = 32
ARC_V2_NONCE_BYTES = 24


def b64encode_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64decode_required(value: object, field_name: str, expected_len: int | None = None) -> bytes:
    if not isinstance(value, str) or not value:
        raise ValueError(f"Encrypted seed file is missing {field_name}.")
    try:
        data = base64.b64decode(value, validate=True)
    except Exception as e:
        raise ValueError(f"Encrypted seed file has invalid {field_name}.") from e
    if expected_len is not None and len(data) != expected_len:
        raise ValueError(f"Encrypted seed file has invalid {field_name} length.")
    return data


def arc_v2_stream_crypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """Encrypt/decrypt with an HMAC-SHA512 counter stream.

    Python stdlib has no AES-GCM or block cipher. This keeps the implementation
    dependency-free while pairing the stream with a separate HMAC-SHA512 tag.
    """
    out = bytearray()
    counter = 0
    while len(out) < len(data):
        msg = b"Arculus ARC v2 stream\x00" + nonce + counter.to_bytes(8, "big")
        out.extend(hmac.new(key, msg, hashlib.sha512).digest())
        counter += 1
    return bytes(a ^ b for a, b in zip(data, out[: len(data)]))


def arc_v2_keys(password: str, salt: bytes, iterations: int) -> Tuple[bytes, bytes]:
    if iterations < ARC_V2_MIN_KDF_ITERATIONS:
        raise ValueError("Encrypted seed file uses too few KDF iterations.")
    password_bytes = normalize_nfkd(password).encode("utf-8")
    master_key = hashlib.pbkdf2_hmac("sha512", password_bytes, salt, iterations, dklen=64)
    enc_key = hmac.new(master_key, b"Arculus ARC v2 encryption key", hashlib.sha512).digest()
    mac_key = hmac.new(master_key, b"Arculus ARC v2 authentication key", hashlib.sha512).digest()
    return enc_key, mac_key


def arc_v2_mac_data(bundle: Dict, salt: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    kdf = bundle.get("kdf", {})
    cipher = bundle.get("cipher", {})
    parts = [
        b"Arculus ARC v2 MAC",
        str(bundle.get("magic", "")).encode("utf-8"),
        str(bundle.get("format", "")).encode("utf-8"),
        str(bundle.get("version", "")).encode("utf-8"),
        str(bundle.get("created_at", "")).encode("utf-8"),
        str(kdf.get("name", "")).encode("utf-8"),
        str(kdf.get("hash", "")).encode("utf-8"),
        str(kdf.get("iterations", "")).encode("utf-8"),
        str(cipher.get("name", "")).encode("utf-8"),
        salt,
        nonce,
        ciphertext,
    ]
    return b"\x00".join(parts)


def normalize_decrypted_mnemonic(payload: Dict) -> str:
    if not isinstance(payload, dict):
        raise ValueError("Encrypted seed file contents are invalid.")
    mnemonic = " ".join(normalize_mnemonic_words(str(payload.get("mnemonic", ""))))
    if not mnemonic:
        raise ValueError("Encrypted seed file did not contain a mnemonic.")
    expected_count = payload.get("word_count")
    if expected_count is not None and int(expected_count) != len(normalize_mnemonic_words(mnemonic)):
        raise ValueError("Encrypted seed file word count does not match mnemonic.")
    return mnemonic


def encrypt_v2(mnemonic: str, password: str) -> Dict:
    """Create a modern `.arc` bundle using PBKDF2-SHA512 and HMAC-SHA512 AE."""
    words = normalize_mnemonic_words(mnemonic)
    if len(words) not in (12, 24):
        raise ValueError("Only 12-word and 24-word mnemonics can be encrypted.")
    salt = os.urandom(ARC_V2_SALT_BYTES)
    nonce = os.urandom(ARC_V2_NONCE_BYTES)
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    bundle = {
        "magic": ARC_MAGIC,
        "format": ARC_V2_FORMAT,
        "version": 2,
        "created_at": created_at,
        "kdf": {
            "name": "PBKDF2",
            "hash": "SHA-512",
            "iterations": ARC_V2_KDF_ITERATIONS,
            "salt_b64": b64encode_bytes(salt),
        },
        "cipher": {
            "name": "HMAC-SHA512-CTR",
            "nonce_b64": b64encode_bytes(nonce),
        },
    }
    payload = {
        "mnemonic": " ".join(words),
        "word_count": len(words),
        "created_at": created_at,
    }
    plaintext = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    enc_key, mac_key = arc_v2_keys(password, salt, ARC_V2_KDF_ITERATIONS)
    ciphertext = arc_v2_stream_crypt(plaintext, enc_key, nonce)
    bundle["ciphertext_b64"] = b64encode_bytes(ciphertext)
    mac = hmac.new(mac_key, arc_v2_mac_data(bundle, salt, nonce, ciphertext), hashlib.sha512).digest()
    bundle["mac_b64"] = b64encode_bytes(mac)
    return bundle


def decrypt_v2(bundle: Dict, password: str) -> str:
    if bundle.get("magic") != ARC_MAGIC or bundle.get("version") != 2 or bundle.get("format") != ARC_V2_FORMAT:
        raise ValueError("Unsupported encrypted seed file format.")
    kdf = bundle.get("kdf")
    cipher = bundle.get("cipher")
    if not isinstance(kdf, dict) or not isinstance(cipher, dict):
        raise ValueError("Encrypted seed file is malformed.")
    if kdf.get("name") != "PBKDF2" or kdf.get("hash") != "SHA-512":
        raise ValueError("Unsupported encrypted seed file KDF.")
    if cipher.get("name") != "HMAC-SHA512-CTR":
        raise ValueError("Unsupported encrypted seed file cipher.")
    try:
        iterations = int(kdf.get("iterations"))
    except Exception as e:
        raise ValueError("Encrypted seed file has invalid KDF iterations.") from e
    salt = b64decode_required(kdf.get("salt_b64"), "salt_b64", ARC_V2_SALT_BYTES)
    nonce = b64decode_required(cipher.get("nonce_b64"), "nonce_b64", ARC_V2_NONCE_BYTES)
    ciphertext = b64decode_required(bundle.get("ciphertext_b64"), "ciphertext_b64")
    expected_mac = b64decode_required(bundle.get("mac_b64"), "mac_b64", 64)
    enc_key, mac_key = arc_v2_keys(password, salt, iterations)
    actual_mac = hmac.new(mac_key, arc_v2_mac_data(bundle, salt, nonce, ciphertext), hashlib.sha512).digest()
    if not hmac.compare_digest(actual_mac, expected_mac):
        raise ValueError("Unable to decrypt seed file. The password may be incorrect or the file may be corrupted.")
    plaintext = arc_v2_stream_crypt(ciphertext, enc_key, nonce)
    try:
        payload = json.loads(plaintext.decode("utf-8"))
    except Exception as e:
        raise ValueError("Encrypted seed file contents are invalid.") from e
    return normalize_decrypted_mnemonic(payload)


def decrypt_v1(bundle: Dict, password: str) -> str:
    if bundle.get("format") not in ("arculus-encrypted-seed-v2", "arculus-encrypted-seed-python-v1"):
        raise ValueError("Unsupported encrypted seed file format.")
    try:
        iterations = int(bundle["kdf"]["iterations"])
        salt = base64.b64decode(bundle["kdf"]["salt_b64"])
        nonce = base64.b64decode(bundle["cipher"]["nonce_b64"])
        ciphertext = base64.b64decode(bundle["ciphertext_b64"])
        expected_mac = base64.b64decode(bundle["mac_b64"])
    except Exception as e:
        raise ValueError("Encrypted seed file is malformed.") from e
    password_bytes = normalize_nfkd(password).encode("utf-8")
    derived = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, iterations, dklen=64)
    enc_key, mac_key = derived[:32], derived[32:]
    actual_mac = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(actual_mac, expected_mac):
        raise ValueError("Unable to decrypt seed file. The password may be incorrect or the file may be corrupted.")
    plaintext = xor_stream_crypt(ciphertext, enc_key, nonce)
    try:
        payload = json.loads(plaintext.decode("utf-8"))
    except Exception as e:
        raise ValueError("Encrypted seed file contents are invalid.") from e
    return normalize_decrypted_mnemonic(payload)


def encrypt_seed_bundle(mnemonic: str, password: str) -> Dict:
    return encrypt_v2(mnemonic, password)


def decrypt_seed_bundle(bundle: Dict, password: str) -> str:
    return decrypt(bundle, password)


def serialize_seed_bundle(bundle: Dict) -> str:
    payload = json.dumps(bundle, separators=(",", ":"), sort_keys=True).encode("utf-8")
    encoded = base64.b64encode(payload).decode("ascii")
    return f"{ARC_ARMOR_HEADER}\n{encoded}\n"


def parse_seed_bundle(text: str) -> Dict:
    stripped = text.strip()
    if stripped.startswith(ARC_ARMOR_HEADER):
        encoded = "".join(stripped.splitlines()[1:]).strip()
        try:
            decoded = base64.b64decode(encoded, validate=True)
            return json.loads(decoded.decode("utf-8"))
        except Exception as e:
            raise ValueError("Selected encrypted seed file armor is invalid.") from e
    try:
        return json.loads(text)
    except Exception as e:
        raise ValueError("Selected file is not a supported encrypted seed file.") from e


def decrypt(bundle: Dict, password: str) -> str:
    if not isinstance(bundle, dict):
        raise ValueError("Unsupported encrypted seed file format.")
    if bundle.get("magic") == ARC_MAGIC or bundle.get("version") == 2:
        return decrypt_v2(bundle, password)
    return decrypt_v1(bundle, password)


def encrypt_seed_bundle_v1(mnemonic: str, password: str) -> Dict:
    salt = os.urandom(16)
    nonce = os.urandom(16)
    password_bytes = normalize_nfkd(password).encode("utf-8")
    derived = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 250000, dklen=64)
    enc_key, mac_key = derived[:32], derived[32:]
    words = normalize_mnemonic_words(mnemonic)
    payload = {
        "mnemonic": " ".join(words),
        "word_count": len(words),
    }
    plaintext = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ciphertext = xor_stream_crypt(plaintext, enc_key, nonce)
    mac = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
    return {
        "format": "arculus-encrypted-seed-v2",
        "kdf": {
            "name": "PBKDF2",
            "hash": "SHA-256",
            "iterations": 250000,
            "salt_b64": base64.b64encode(salt).decode("ascii"),
        },
        "cipher": {
            "name": "XOR-HMAC-SHA256",
            "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        },
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
        "mac_b64": base64.b64encode(mac).decode("ascii"),
    }


def parse_path(path: str) -> List[int]:
    if not path:
        return []
    elems = path.strip().split("/")
    if elems[0] == "m":
        elems = elems[1:]
    out = []
    for e in elems:
        if e == "":
            continue
        hardened = False
        if e.endswith("'") or e.endswith("h") or e.endswith("H"):
            hardened = True
            e = e[:-1]
        i = int(e)
        if i < 0 or i >= HARDENED:
            raise ValueError(f"invalid path index: {i}")
        if hardened:
            i |= HARDENED
        out.append(i)
    return out


def normalize_path(path: str) -> str:
    ints = parse_path(path)
    if not ints:
        return "m"
    parts = []
    for i in ints:
        parts.append(f"{i - HARDENED}'" if (i & HARDENED) else str(i))
    return "m/" + "/".join(parts)


def purpose_to_script_type(path: str) -> str:
    ints = parse_path(path)
    if not ints:
        return "p2pkh"
    purpose = ints[0] & 0x7FFFFFFF
    if purpose == 44:
        return "p2pkh"
    if purpose == 49:
        return "p2wpkh-p2sh"
    if purpose == 84:
        return "p2wpkh"
    if purpose == 86:
        return "p2tr"
    return "p2pkh"


@dataclass
class ExtPrv:
    k: int
    c: bytes
    depth: int
    parent_fp: bytes
    child_num: int

    def pub(self):
        return point_mul(self.k, G)


def master_from_seed(seed: bytes) -> ExtPrv:
    I = hmac_sha512(b"Bitcoin seed", seed)
    IL, IR = I[:32], I[32:]
    k = int.from_bytes(IL, "big")
    if k == 0 or k >= N:
        raise ValueError("invalid master key")
    return ExtPrv(k=k, c=IR, depth=0, parent_fp=b"\x00\x00\x00\x00", child_num=0)


def ckd_priv(node: ExtPrv, index: int) -> ExtPrv:
    data = (b"\x00" + ser256(node.k) if (index & HARDENED) else ser_pubkey(node.pub())) + ser32(index)
    I = hmac_sha512(node.c, data)
    IL, IR = I[:32], I[32:]
    il_int = int.from_bytes(IL, "big")
    child_k = (il_int + node.k) % N
    if il_int >= N or child_k == 0:
        raise ValueError("invalid child key")
    fp = hash160(ser_pubkey(node.pub()))[:4]
    return ExtPrv(k=child_k, c=IR, depth=node.depth + 1, parent_fp=fp, child_num=index)


def derive(node: ExtPrv, path: str) -> ExtPrv:
    out = node
    for i in parse_path(path):
        out = ckd_priv(out, i)
    return out


def ext_prv_to_base58(node: ExtPrv, version: int) -> str:
    payload = (
        version.to_bytes(4, "big")
        + bytes([node.depth])
        + node.parent_fp
        + ser32(node.child_num)
        + node.c
        + b"\x00"
        + ser256(node.k)
    )
    return b58check(payload)


def ext_pub_to_base58(node: ExtPrv, version: int) -> str:
    payload = (
        version.to_bytes(4, "big")
        + bytes([node.depth])
        + node.parent_fp
        + ser32(node.child_num)
        + node.c
        + ser_pubkey(node.pub())
    )
    return b58check(payload)


def to_wif(privkey: int, netcfg: dict) -> str:
    return b58check(bytes([netcfg["wif"]]) + ser256(privkey) + b"\x01")


def taproot_key_material(privkey: int) -> Dict:
    pub = point_mul(privkey, G)
    if pub is None:
        raise ValueError("invalid Taproot internal key")
    if pub[1] & 1:
        internal_priv = (N - privkey) % N
        internal_pub = negate_point(pub)
    else:
        internal_priv = privkey
        internal_pub = pub
    tweak = int.from_bytes(tagged_hash("TapTweak", xonly_pubkey(internal_pub)), "big")
    if tweak >= N:
        raise ValueError("invalid Taproot tweak")
    output_pub = point_add(internal_pub, point_mul(tweak, G))
    if output_pub is None:
        raise ValueError("invalid Taproot output key")
    output_priv = (internal_priv + tweak) % N
    if output_priv == 0:
        raise ValueError("invalid Taproot private key")
    return {
        "internal_private_key": internal_priv,
        "internal_public_key": xonly_pubkey(internal_pub),
        "tweak": tweak.to_bytes(32, "big"),
        "output_private_key": output_priv,
        "output_public_key": xonly_pubkey(output_pub),
        "output_key_parity": output_pub[1] & 1,
    }


def pubkey_to_address(pubkey: bytes, script_type: str, netcfg: dict) -> str:
    pkh = hash160(pubkey)
    if script_type == "p2pkh":
        return b58check(bytes([netcfg["p2pkh_prefix"]]) + pkh)
    if script_type == "p2wpkh":
        return segwit_addr_v0(netcfg["hrp"], pkh)
    if script_type == "p2wpkh-p2sh":
        redeem = b"\x00\x14" + pkh
        return b58check(bytes([netcfg["p2sh_prefix"]]) + hash160(redeem))
    if script_type == "p2tr":
        raise ValueError("taproot addresses require Taproot key material")
    raise ValueError(f"unsupported script type: {script_type}")


def derive_account(mnemonic: str, passphrase: str, derivation: str, script_type: str, count: int, netcfg: dict):
    seed = bip39_to_seed(mnemonic, passphrase)
    root = master_from_seed(seed)
    account = derive(root, derivation)
    st = purpose_to_script_type(derivation) if script_type == "auto" else script_type
    root_versions = netcfg["p2pkh"]
    x_versions = netcfg["p2pkh"]
    y_versions = netcfg["p2wpkh-p2sh"]
    z_versions = netcfg["p2wpkh"]
    tr_versions = netcfg["p2tr"]
    if st == "p2tr" and not tr_versions:
        raise ValueError("taproot is not supported for this coin/network")

    result = {
        "derivation": derivation,
        "account_script_type_used": st,
        "root_xprv": ext_prv_to_base58(root, root_versions["xprv"]),
        "root_xpub": ext_pub_to_base58(root, root_versions["xpub"]),
    }
    if st == "p2wpkh-p2sh":
        result["root_yprv"] = ext_prv_to_base58(root, y_versions["xprv"])
        result["root_ypub"] = ext_pub_to_base58(root, y_versions["xpub"])
    elif st == "p2wpkh":
        result["root_zprv"] = ext_prv_to_base58(root, z_versions["xprv"])
        result["root_zpub"] = ext_pub_to_base58(root, z_versions["xpub"])
    elif st == "p2tr" and tr_versions:
        result["root_trprv"] = ext_prv_to_base58(root, tr_versions["xprv"])
        result["root_trpub"] = ext_pub_to_base58(root, tr_versions["xpub"])
    result["account_xprv"] = ext_prv_to_base58(account, x_versions["xprv"])
    result["account_xpub"] = ext_pub_to_base58(account, x_versions["xpub"])
    if st == "p2wpkh-p2sh":
        result["account_yprv"] = ext_prv_to_base58(account, y_versions["xprv"])
        result["account_ypub"] = ext_pub_to_base58(account, y_versions["xpub"])
    elif st == "p2wpkh":
        result["account_zprv"] = ext_prv_to_base58(account, z_versions["xprv"])
        result["account_zpub"] = ext_pub_to_base58(account, z_versions["xpub"])
    elif st == "p2tr" and tr_versions:
        result["account_trprv"] = ext_prv_to_base58(account, tr_versions["xprv"])
        result["account_trpub"] = ext_pub_to_base58(account, tr_versions["xpub"])
    result["receiving"] = []
    result["change"] = []

    for branch, key in ((0, "receiving"), (1, "change")):
        branch_node = ckd_priv(account, branch)
        for i in range(count):
            child = ckd_priv(branch_node, i)
            pub = ser_pubkey(child.pub())
            item = {
                "path": f"{derivation}/{branch}/{i}",
                "address": None if st == "p2tr" else pubkey_to_address(pub, st, netcfg),
                "public_key_hex": pub.hex(),
                "private_key_hex": ser256(child.k).hex(),
                "private_key_wif": to_wif(child.k, netcfg),
            }
            if st == "p2tr":
                taproot = taproot_key_material(child.k)
                item["address"] = segwit_addr_v1(netcfg["hrp"], taproot["output_public_key"])
                item["taproot_internal_public_key_hex"] = taproot["internal_public_key"].hex()
                item["taproot_internal_private_key_hex"] = ser256(taproot["internal_private_key"]).hex()
                item["taproot_internal_private_key_wif"] = to_wif(taproot["internal_private_key"], netcfg)
                item["taproot_tweak_hex"] = taproot["tweak"].hex()
                item["taproot_output_public_key_hex"] = taproot["output_public_key"].hex()
                item["taproot_output_private_key_hex"] = ser256(taproot["output_private_key"]).hex()
                item["taproot_output_private_key_wif"] = to_wif(taproot["output_private_key"], netcfg)
                item["taproot_output_key_parity"] = taproot["output_key_parity"]
            result[key].append(item)
    return result


def run_derivation(
    mnemonic: str,
    passphrase: str,
    derivation: str,
    all_common: bool,
    script_type: str,
    count: int,
    coin: str,
    testnet: bool,
) -> Dict:
    words_ok, checksum_ok, msg = bip39_validate(mnemonic)
    if not words_ok:
        raise ValueError(msg)
    if not checksum_ok:
        raise ValueError(msg)
    if count < 1:
        raise ValueError("--count must be >= 1")

    coin_key = coin.strip().lower()
    if coin_key not in COINS:
        raise ValueError(f"unsupported coin: {coin}")
    coin_cfg = COINS[coin_key]
    if testnet:
        if coin_cfg["testnet"] is None:
            raise ValueError(f"testnet is not configured for {coin_key}")
        netcfg = coin_cfg["testnet"]
    else:
        netcfg = coin_cfg["mainnet"]

    coin_type = coin_cfg["coin_type"]
    base_derivation = (derivation or "").strip() or DEFAULT_ACCOUNT_DERIVATION[coin_key]
    derivations = (
        [f"m/44'/{coin_type}'/0'", f"m/49'/{coin_type}'/0'", f"m/84'/{coin_type}'/0'", f"m/86'/{coin_type}'/0'"] if all_common else [base_derivation]
    )
    derivations = [normalize_path(d) for d in derivations]

    out = {
        "coin": coin_key,
        "network": "testnet" if testnet else "mainnet",
        "word_count": len(normalize_mnemonic_words(mnemonic)),
        "accounts": [],
    }
    for d in derivations:
        out["accounts"].append(derive_account(mnemonic, passphrase, d, script_type, count, netcfg))
    return out


def flatten_derived_rows(data: Dict) -> List[Dict]:
    rows = []
    for account in data.get("accounts", []):
        account_fields = {k: v for k, v in account.items() if k not in ("receiving", "change")}
        for branch in ("receiving", "change"):
            for item in account.get(branch, []):
                rows.append(
                    {
                        "coin": data.get("coin"),
                        "network": data.get("network"),
                        "word_count": data.get("word_count"),
                        "branch": branch,
                        **account_fields,
                        **item,
                    }
                )
    return rows


def derived_to_csv(data: Dict) -> str:
    rows = flatten_derived_rows(data)
    if not rows:
        return ""
    headers = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def text_label(key: str) -> str:
    return key.replace("_", " ")


def append_text_fields(lines: List[str], obj: Dict, exclude: Tuple[str, ...] = ()) -> None:
    excluded = set(exclude)
    for key, value in (obj or {}).items():
        if key in excluded or value is None:
            continue
        lines.append(f"{text_label(key)}: {value}")


def derived_to_text(data: Dict) -> str:
    lines = [
        "Arculus Derived Keys and Addresses",
        "",
        f"coin: {data.get('coin', '')}",
        f"network: {data.get('network', '')}",
        f"word count: {data.get('word_count', '')}",
    ]
    for account_index, account in enumerate(data.get("accounts", []), start=1):
        lines.extend(["", f"Account {account_index}"])
        append_text_fields(lines, account, ("receiving", "change"))
        for branch in ("receiving", "change"):
            lines.extend(["", f"{branch.capitalize()} Addresses"])
            items = account.get(branch, [])
            if not items:
                lines.append("No addresses derived.")
                continue
            for item_index, item in enumerate(items):
                lines.extend(["", f"{branch} #{item_index}"])
                append_text_fields(lines, item)
    return "\n".join(lines) + "\n"


def format_derived_output(data: Dict, output_format: str) -> str:
    fmt = output_format.lower()
    if fmt == "csv":
        return derived_to_csv(data)
    if fmt == "txt":
        return derived_to_text(data)
    return json.dumps(data, indent=2) + "\n"


def launch_gui() -> None:
    import tkinter as tk
    import tkinter.font as tkfont
    from tkinter import filedialog, messagebox, simpledialog
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText

    root = tk.Tk()
    root.title("Arculus Recovery")
    root.geometry("1080x840")

    frm = ttk.Frame(root, padding=10)
    frm.pack(fill=tk.BOTH, expand=True)
    frm.columnconfigure(1, weight=1)
    frm.rowconfigure(11, weight=1)

    normal_font = tkfont.nametofont("TkDefaultFont").copy()
    bold_font = tkfont.nametofont("TkDefaultFont").copy()
    bold_font.configure(weight="bold")
    title_font = tkfont.nametofont("TkDefaultFont").copy()
    title_font.configure(size=16, weight="bold")
    valid_color = "#1b8f2f"
    invalid_color = "#b71c1c"
    current_theme = {
        "colors": {
            "bg": "#f7f8fa",
            "card": "#ffffff",
            "field": "#ffffff",
            "text": "#111827",
            "muted": "#6b7280",
            "button": "#ffffff",
            "border": "#d1d5db",
            "select": "#dbeafe",
        }
    }

    title_row = ttk.Frame(frm)
    title_row.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
    ttk.Label(title_row, text="Arculus Recovery", font=title_font).pack(side=tk.LEFT)
    settings_btn = ttk.Button(title_row, text="Settings")
    settings_btn.pack(side=tk.LEFT, padx=(10, 0))

    ttk.Label(frm, text="Mnemonic (12 or 24 words):").grid(row=1, column=0, sticky="w")
    mnemonic_txt = ScrolledText(frm, height=4, wrap=tk.WORD)
    mnemonic_txt.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
    mnemonic_txt.tag_configure("valid_word", foreground=valid_color, font=bold_font)
    mnemonic_txt.tag_configure("invalid_word", foreground=invalid_color, font=bold_font)

    seed_len_var = tk.IntVar(value=12)
    dark_mode_var = tk.BooleanVar(value=False)
    seed_len_row = ttk.Frame(frm)
    seed_len_row.grid(row=2, column=1, sticky="w", padx=(8, 0), pady=(4, 0))
    ttk.Label(seed_len_row, text="Seed length:").pack(side=tk.LEFT)
    ttk.Radiobutton(seed_len_row, text="12 words", value=12, variable=seed_len_var).pack(side=tk.LEFT, padx=(8, 0))
    ttk.Radiobutton(seed_len_row, text="24 words", value=24, variable=seed_len_var).pack(side=tk.LEFT, padx=(8, 0))
    copy_seed_btn = tk.Button(seed_len_row, text="Copy Seed", bg="#dc2626", fg="#111827", activebackground="#b91c1c", activeforeground="#111827")
    copy_seed_btn.pack(side=tk.LEFT, padx=(14, 0))
    generate_seed_btn = tk.Button(seed_len_row, text="Generate Random Seed", bg="#22c55e", fg="#111827", activebackground="#16a34a", activeforeground="#111827")
    generate_seed_btn.pack(side=tk.LEFT, padx=(8, 0))

    ttk.Label(frm, text="Numbered Words:").grid(row=3, column=0, sticky="nw")
    words_frame = ttk.Frame(frm)
    words_frame.grid(row=3, column=1, sticky="ew", padx=(8, 0), pady=(2, 0))
    for c in range(4):
        words_frame.columnconfigure(c, weight=1)

    word_vars: List[tk.StringVar] = []
    word_entries: List[tk.Entry] = []
    for i in range(24):
        row = i // 4
        col = i % 4
        cell = ttk.Frame(words_frame)
        cell.grid(row=row, column=col, sticky="ew", padx=2, pady=2)
        ttk.Label(cell, text=f"{i + 1}.", width=3).pack(side=tk.LEFT)
        v = tk.StringVar()
        e = tk.Entry(cell, textvariable=v, width=18)
        e.pack(side=tk.LEFT, fill=tk.X, expand=True)
        word_vars.append(v)
        word_entries.append(e)

    ttk.Label(frm, text="Passphrase:").grid(row=4, column=0, sticky="w")
    passphrase_var = tk.StringVar()
    passphrase_entry = ttk.Entry(frm, textvariable=passphrase_var, show="*")
    passphrase_entry.grid(row=4, column=1, sticky="ew", padx=(8, 0))

    ttk.Label(frm, text="Coin:").grid(row=5, column=0, sticky="w")
    coin_label_to_value = {
        "Bitcoin": "bitcoin",
        "Litecoin": "litecoin",
        "Dogecoin": "dogecoin",
    }
    coin_var = tk.StringVar(value="Bitcoin")
    coin_combo = ttk.Combobox(frm, textvariable=coin_var, values=list(coin_label_to_value.keys()), state="readonly")
    coin_combo.grid(
        row=5, column=1, sticky="w", padx=(8, 0)
    )

    ttk.Label(frm, text="Derivation:").grid(row=6, column=0, sticky="w")
    derivation_var = tk.StringVar(value="m/0'")
    derivation_entry = ttk.Entry(frm, textvariable=derivation_var)
    derivation_entry.grid(row=6, column=1, sticky="ew", padx=(8, 0))

    ttk.Label(frm, text="Script Type:").grid(row=7, column=0, sticky="w")
    script_label_to_value = {
        "Auto": "auto",
        "P2PKH": "p2pkh",
        "P2WPKH-P2SH": "p2wpkh-p2sh",
        "P2WPKH": "p2wpkh",
        "P2TR": "p2tr",
    }
    script_var = tk.StringVar(value="P2WPKH")
    ttk.Combobox(frm, textvariable=script_var, values=list(script_label_to_value.keys()), state="readonly").grid(
        row=7, column=1, sticky="w", padx=(8, 0)
    )

    ttk.Label(frm, text="Address Count:").grid(row=8, column=0, sticky="w")
    count_var = tk.StringVar(value="5")
    count_entry = ttk.Entry(frm, textvariable=count_var, width=8)
    count_entry.grid(row=8, column=1, sticky="w", padx=(8, 0))

    status_var = tk.StringVar(value="Ready")
    ttk.Label(frm, textvariable=status_var).grid(row=9, column=0, columnspan=2, sticky="w", pady=(6, 6))

    output = ScrolledText(frm, height=20, wrap=tk.NONE)
    output.grid(row=11, column=0, columnspan=2, sticky="nsew")
    imported_seed_state = {"mnemonic": None, "source_name": None}
    showing_imported_seed = {"active": False}
    root_fingerprint_var = tk.StringVar(value="Root Fingerprint:")
    export_format_var = tk.StringVar(value="JSON")
    last_derived_state = {"data": None}
    settings_window = {"window": None, "frame": None}

    def install_clipboard_bindings(widget: tk.Widget, is_text_widget: bool) -> None:
        menu = tk.Menu(root, tearoff=0)

        def do_cut(_event=None):
            widget.event_generate("<<Cut>>")
            return "break"

        def do_copy(_event=None):
            widget.event_generate("<<Copy>>")
            return "break"

        def do_paste(_event=None):
            widget.event_generate("<<Paste>>")
            return "break"

        def do_select_all(_event=None):
            if is_text_widget:
                widget.tag_add("sel", "1.0", "end-1c")
                widget.mark_set("insert", "1.0")
                widget.see("insert")
            else:
                widget.selection_range(0, tk.END)
                widget.icursor(tk.END)
            return "break"

        menu.add_command(label="Cut", command=lambda: do_cut())
        menu.add_command(label="Copy", command=lambda: do_copy())
        menu.add_command(label="Paste", command=lambda: do_paste())
        menu.add_separator()
        menu.add_command(label="Select All", command=lambda: do_select_all())

        widget.bind("<Control-x>", do_cut)
        widget.bind("<Control-c>", do_copy)
        widget.bind("<Control-v>", do_paste)
        widget.bind("<Control-a>", do_select_all)
        widget.bind("<Button-3>", lambda e: (menu.tk_popup(e.x_root, e.y_root), "break")[1])

    def set_output(text: str) -> None:
        output.delete("1.0", tk.END)
        output.insert(tk.END, text)

    def set_root_fingerprint_display(fingerprint: str = "") -> None:
        root_fingerprint_var.set(f"Root Fingerprint: {fingerprint}" if fingerprint else "Root Fingerprint:")

    def get_active_mnemonic() -> str:
        return imported_seed_state["mnemonic"] or mnemonic_txt.get("1.0", tk.END).strip()

    def has_visible_seed_input() -> bool:
        if mnemonic_txt.get("1.0", tk.END).strip():
            return True
        return any(v.get().strip() for v in word_vars)

    def clear_visible_seed_inputs() -> None:
        sync_guard["busy"] = True
        try:
            mnemonic_txt.delete("1.0", tk.END)
            for v in word_vars:
                v.set("")
            refresh_numbered_entries_style()
            highlight_main_text_words()
            sync_state["last_main_words"] = []
            mnemonic_txt.edit_modified(False)
        finally:
            sync_guard["busy"] = False

    def clear_imported_seed(silent: bool = False) -> None:
        if not imported_seed_state["mnemonic"]:
            return
        imported_seed_state["mnemonic"] = None
        imported_seed_state["source_name"] = None
        showing_imported_seed["active"] = False
        refresh_root_fingerprint_display()
        if not silent:
            status_var.set("Imported encrypted seed cleared.")

    def apply_imported_seed(mnemonic: str, source_name: str) -> None:
        words = normalize_mnemonic_words(mnemonic)
        imported_seed_state["mnemonic"] = " ".join(words)
        imported_seed_state["source_name"] = source_name or "encrypted seed file"
        clear_visible_seed_inputs()
        if len(words) in (12, 24):
            seed_len_var.set(len(words))
        status_var.set("Encrypted seed imported. Seed phrase is hidden but ready for validation and derivation.")
        set_output(
            json.dumps(
                {
                    "imported_seed": "loaded",
                    "source": imported_seed_state["source_name"],
                    "word_count": len(words),
                    "hidden_on_screen": True,
                },
                indent=2,
            )
        )
        refresh_root_fingerprint_display()

    def reveal_imported_seed(_event=None):
        if not imported_seed_state["mnemonic"] or showing_imported_seed["active"]:
            return None
        words = normalize_mnemonic_words(imported_seed_state["mnemonic"])
        showing_imported_seed["active"] = True
        sync_guard["busy"] = True
        try:
            mnemonic_txt.delete("1.0", tk.END)
            mnemonic_txt.insert("1.0", imported_seed_state["mnemonic"])
            if len(words) in (12, 24):
                seed_len_var.set(len(words))
            set_entries_from_main_text()
            highlight_main_text_words()
            mnemonic_txt.edit_modified(False)
        finally:
            sync_guard["busy"] = False
        return "break"

    def hide_imported_seed(_event=None):
        if not imported_seed_state["mnemonic"] or not showing_imported_seed["active"]:
            return None
        showing_imported_seed["active"] = False
        clear_visible_seed_inputs()
        status_var.set("Encrypted seed imported. Seed phrase is hidden but ready for validation and derivation.")
        return "break"

    def refresh_root_fingerprint_display(*_args) -> None:
        mnemonic = get_active_mnemonic()
        words = normalize_mnemonic_words(mnemonic)
        if len(words) not in (12, 24):
            set_root_fingerprint_display("")
            return
        try:
            analysis = analyze_mnemonic(mnemonic, passphrase_var.get())
            set_root_fingerprint_display(analysis.get("root_fingerprint") or "")
        except Exception:
            set_root_fingerprint_display("")

    def on_mnemonic_modified(_event=None) -> None:
        # Handle typing, paste, and programmatic text updates consistently.
        if mnemonic_txt.edit_modified():
            mnemonic_txt.edit_modified(False)
            on_main_text_change()

    sync_guard = {"busy": False}
    sync_state = {"last_main_words": []}

    def style_entry_for_word(entry: tk.Entry, raw_word: str, enabled: bool) -> None:
        theme = current_theme["colors"]
        if not enabled:
            entry.configure(
                state="disabled",
                fg=theme["muted"],
                disabledforeground=theme["muted"],
                bg=theme["field"],
                font=normal_font,
                insertbackground=theme["text"],
            )
            return
        entry.configure(state="normal", bg=theme["field"], insertbackground=theme["text"])
        word = normalize_nfkd(raw_word.strip().lower())
        if word == "":
            entry.configure(fg=theme["text"], font=normal_font)
        elif word in BIP39_WORD_INDEX:
            entry.configure(fg=valid_color, font=bold_font)
        else:
            entry.configure(fg=invalid_color, font=bold_font)

    def highlight_main_text_words() -> None:
        mnemonic_txt.tag_remove("valid_word", "1.0", tk.END)
        mnemonic_txt.tag_remove("invalid_word", "1.0", tk.END)
        text = mnemonic_txt.get("1.0", tk.END)
        for m in re.finditer(r"\S+", text):
            word = normalize_nfkd(m.group(0).strip().lower())
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            if word in BIP39_WORD_INDEX:
                mnemonic_txt.tag_add("valid_word", start, end)
            else:
                mnemonic_txt.tag_add("invalid_word", start, end)

    def refresh_numbered_entries_style() -> None:
        max_words = seed_len_var.get()
        for i, e in enumerate(word_entries):
            style_entry_for_word(e, word_vars[i].get(), i < max_words)

    def set_entries_from_main_text() -> None:
        words = normalize_mnemonic_words(mnemonic_txt.get("1.0", tk.END).strip())
        max_words = seed_len_var.get()
        for i in range(24):
            word_vars[i].set(words[i] if i < len(words) and i < max_words else "")
        refresh_numbered_entries_style()

    def set_main_text_from_entries() -> None:
        max_words = seed_len_var.get()
        words = [normalize_nfkd(word_vars[i].get().strip().lower()) for i in range(max_words)]
        joined = " ".join(w for w in words if w)
        mnemonic_txt.delete("1.0", tk.END)
        mnemonic_txt.insert("1.0", joined)
        highlight_main_text_words()

    def on_main_text_change(_event=None) -> None:
        if sync_guard["busy"]:
            return
        sync_guard["busy"] = True
        try:
            if imported_seed_state["mnemonic"] and not showing_imported_seed["active"] and has_visible_seed_input():
                clear_imported_seed(silent=True)
            words = normalize_mnemonic_words(mnemonic_txt.get("1.0", tk.END).strip())
            wc = len([w for w in words if w])
            # Auto-detect seed length only while user is actively editing
            # the mnemonic box. This prevents manual 12/24 selection from
            # being immediately overridden by sync updates.
            if root.focus_get() == mnemonic_txt:
                # 1-12 words -> 12 mode, 13+ words -> 24 mode.
                if wc > 12:
                    seed_len_var.set(24)
                elif wc > 0:
                    seed_len_var.set(12)
            highlight_main_text_words()
            max_words = seed_len_var.get()
            current_slots = [normalize_nfkd(word_vars[i].get().strip().lower()) for i in range(max_words)]
            current_compact = [w for w in current_slots if w]
            prev_words = sync_state["last_main_words"]

            # If words were deleted from main box, preserve numbered-word positions by
            # blanking the removed slot instead of shifting everything left.
            if prev_words and wc < len(prev_words) and wc <= len(current_compact):
                mismatch = 0
                while mismatch < len(words) and mismatch < len(current_compact) and words[mismatch] == current_compact[mismatch]:
                    mismatch += 1
                nonempty_indices = [i for i, w in enumerate(current_slots) if w]
                if nonempty_indices:
                    if mismatch < len(nonempty_indices):
                        slot_to_clear = nonempty_indices[mismatch]
                    else:
                        slot_to_clear = nonempty_indices[-1]
                    word_vars[slot_to_clear].set("")
                    refresh_numbered_entries_style()
                else:
                    set_entries_from_main_text()
            else:
                set_entries_from_main_text()
            sync_state["last_main_words"] = words
        finally:
            sync_guard["busy"] = False
        refresh_root_fingerprint_display()

    def on_entry_change(_event=None) -> None:
        if sync_guard["busy"]:
            return
        sync_guard["busy"] = True
        try:
            if imported_seed_state["mnemonic"] and not showing_imported_seed["active"] and has_visible_seed_input():
                clear_imported_seed(silent=True)
            refresh_numbered_entries_style()
            set_main_text_from_entries()
        finally:
            sync_guard["busy"] = False
        refresh_root_fingerprint_display()

    def on_seed_length_change() -> None:
        if sync_guard["busy"]:
            return
        sync_guard["busy"] = True
        try:
            max_words = seed_len_var.get()
            for i in range(24):
                if i >= max_words:
                    word_vars[i].set("")
            refresh_numbered_entries_style()
            if imported_seed_state["mnemonic"] and not showing_imported_seed["active"] and not has_visible_seed_input():
                sync_state["last_main_words"] = []
                return
            set_main_text_from_entries()
            sync_state["last_main_words"] = normalize_mnemonic_words(mnemonic_txt.get("1.0", tk.END).strip())
        finally:
            sync_guard["busy"] = False
        refresh_root_fingerprint_display()

    def on_validate() -> None:
        mnemonic = get_active_mnemonic()
        analysis = analyze_mnemonic(mnemonic, passphrase_var.get())
        set_root_fingerprint_display(analysis.get("root_fingerprint") or "")
        status_var.set(analysis["message"])
        set_output(
            json.dumps(
                {
                    "validation": "ok" if analysis["words_ok"] and analysis["checksum_ok"] else "failed",
                    "word_count": analysis["word_count"],
                    "wordlist_validity": analysis["wordlist_validity"],
                    "entropy_bits": analysis["entropy_bits"],
                    "checksum_bits": analysis["checksum_bits"],
                    "checksum_match": analysis["checksum_match"],
                    "bip39_compliance": analysis["bip39_compliance"],
                    "bip39_seed_512_bit": analysis["bip39_seed_512_bit"],
                    "master_private_key": analysis["master_private_key"],
                    "master_chain_code": analysis["master_chain_code"],
                    "root_fingerprint": analysis["root_fingerprint"],
                    "keystore_type": analysis["keystore_type"],
                    "seed_format_detection": analysis["seed_format_detection"],
                    "passphrase_warning": analysis["passphrase_warning"],
                    "message": analysis["message"],
                },
                indent=2,
            )
        )

    def on_derive() -> None:
        try:
            mnemonic = get_active_mnemonic()
            data = run_derivation(
                mnemonic=mnemonic,
                passphrase=passphrase_var.get(),
                derivation=derivation_var.get().strip(),
                all_common=False,
                script_type=script_label_to_value.get(script_var.get(), "p2wpkh"),
                count=int(count_var.get()),
                coin=coin_label_to_value.get(coin_var.get(), "bitcoin"),
                testnet=False,
            )
            last_derived_state["data"] = data
            status_var.set("Derivation complete.")
            set_output(json.dumps(data, indent=2))
        except Exception as e:
            status_var.set(f"Error: {e}")
            set_output(json.dumps({"error": str(e)}, indent=2))

    def on_coin_change(_event=None) -> None:
        selected_coin = coin_label_to_value.get(coin_var.get(), "bitcoin")
        derivation_var.set(DEFAULT_ACCOUNT_DERIVATION[selected_coin])
        if selected_coin == "dogecoin":
            script_var.set("P2PKH")
        else:
            script_var.set("P2WPKH")

    def on_export() -> None:
        data = last_derived_state["data"]
        if not data:
            status_var.set("Nothing to export. Derive keys and addresses first.")
            return
        fmt = export_format_var.get().lower()
        if fmt == "csv":
            text = derived_to_csv(data)
            defaultextension = ".csv"
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
            initialfile = "Arculus_Derived_Keys_Addresses.csv"
        elif fmt == "txt":
            text = derived_to_text(data)
            defaultextension = ".txt"
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
            initialfile = "Arculus_Derived_Keys_Addresses.txt"
        else:
            text = json.dumps(data, indent=2) + "\n"
            defaultextension = ".json"
            filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
            initialfile = "Arculus_Derived_Keys_Addresses.json"
        path = filedialog.asksaveasfilename(
            title="Export Derived Keys/Addresses",
            defaultextension=defaultextension,
            filetypes=filetypes,
            initialfile=initialfile,
        )
        if not path:
            status_var.set("Export canceled.")
            return
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        status_var.set(f"Exported derived keys/addresses as {fmt.upper()} to: {path}")

    def on_encrypt_export_seed() -> None:
        try:
            mnemonic = get_active_mnemonic()
            words_ok, checksum_ok, _ = bip39_validate(mnemonic)
            if not (words_ok and checksum_ok):
                raise ValueError("Load a valid mnemonic before exporting an encrypted seed file.")
            password = simpledialog.askstring("Encrypt/Export Seed", "Enter a password to encrypt this seed export file:", show="*")
            if password is None:
                status_var.set("Encrypted seed export canceled.")
                return
            if password == "":
                raise ValueError("Encryption password cannot be empty.")
            confirm = simpledialog.askstring("Encrypt/Export Seed", "Re-enter the password to confirm:", show="*")
            if confirm is None:
                status_var.set("Encrypted seed export canceled.")
                return
            if password != confirm:
                raise ValueError("Passwords did not match.")
            bundle = encrypt_seed_bundle(mnemonic, password)
            path = filedialog.asksaveasfilename(
                title="Encrypt/Export Seed",
                defaultextension=".arc",
                filetypes=[("Encrypted seed files", "*.arc"), ("JSON files", "*.json"), ("All files", "*.*")],
                initialfile="Arculus_Encrypted_Seed.arc",
            )
            if not path:
                status_var.set("Encrypted seed export canceled.")
                return
            with open(path, "w", encoding="utf-8") as f:
                f.write(serialize_seed_bundle(bundle))
            status_var.set(f"Encrypted seed exported to: {path}")
        except Exception as e:
            status_var.set(f"Error: {e}")
            set_output(json.dumps({"error": str(e)}, indent=2))

    def on_import_seed() -> None:
        try:
            path = filedialog.askopenfilename(
                title="Import Seed",
                filetypes=[("Encrypted seed files", "*.arc"), ("JSON files", "*.json"), ("All files", "*.*")],
            )
            if not path:
                status_var.set("Import canceled.")
                return
            password = simpledialog.askstring("Import Seed", "Enter the password for this encrypted seed file:", show="*")
            if password is None:
                status_var.set("Import canceled.")
                return
            if password == "":
                raise ValueError("Import password cannot be empty.")
            with open(path, "r", encoding="utf-8") as f:
                bundle = parse_seed_bundle(f.read())
            mnemonic = decrypt_seed_bundle(bundle, password)
            words_ok, checksum_ok, msg = bip39_validate(mnemonic)
            if not (words_ok and checksum_ok):
                raise ValueError(f"Imported file decrypted successfully, but the mnemonic is not valid BIP-39. {msg}")
            apply_imported_seed(mnemonic, os.path.basename(path))
        except Exception as e:
            status_var.set(f"Error: {e}")
            set_output(json.dumps({"error": str(e)}, indent=2))

    def on_copy_seed() -> None:
        try:
            mnemonic = get_active_mnemonic()
            words = normalize_mnemonic_words(mnemonic)
            if not words:
                raise ValueError("No seed phrase is currently loaded.")
            ok = messagebox.askokcancel(
                "Copy Seed",
                "Copying a seed phrase to the clipboard is not recommended because other apps or malware may be able to read it. "
                "Only continue if you understand the risk.",
            )
            if not ok:
                status_var.set("Copy seed canceled.")
                return
            root.clipboard_clear()
            root.clipboard_append(" ".join(words))
            root.update()
            status_var.set("Seed phrase copied to clipboard.")
        except Exception as e:
            status_var.set(f"Error: {e}")
            set_output(json.dumps({"error": str(e)}, indent=2))

    def on_generate_seed() -> None:
        try:
            clear_imported_seed(silent=True)
            word_count = seed_len_var.get()
            mnemonic = generate_random_mnemonic(word_count)
            sync_guard["busy"] = True
            try:
                mnemonic_txt.delete("1.0", tk.END)
                mnemonic_txt.insert("1.0", mnemonic)
                seed_len_var.set(word_count)
                set_entries_from_main_text()
                highlight_main_text_words()
                mnemonic_txt.edit_modified(False)
                sync_state["last_main_words"] = normalize_mnemonic_words(mnemonic)
            finally:
                sync_guard["busy"] = False
            refresh_root_fingerprint_display()
            status_var.set(f"Generated random {word_count}-word mnemonic.")
        except Exception as e:
            status_var.set(f"Error: {e}")
            set_output(json.dumps({"error": str(e)}, indent=2))

    copy_seed_btn.configure(command=on_copy_seed)
    generate_seed_btn.configure(command=on_generate_seed)

    btns = ttk.Frame(frm)
    btns.grid(row=10, column=0, columnspan=2, sticky="w", pady=(8, 0))
    ttk.Button(btns, text="Validate Mnemonic", command=on_validate).pack(side=tk.LEFT)
    ttk.Button(btns, text="Derive Keys + Addresses", command=on_derive).pack(side=tk.LEFT, padx=(8, 0))
    ttk.Button(btns, text="Export", command=on_export).pack(side=tk.LEFT, padx=(8, 0))
    ttk.Combobox(btns, textvariable=export_format_var, values=["JSON", "CSV", "TXT"], state="readonly", width=6).pack(side=tk.LEFT, padx=(4, 0))
    ttk.Button(btns, text="Encrypt/Export Seed", command=on_encrypt_export_seed).pack(side=tk.LEFT, padx=(8, 0))
    ttk.Button(btns, text="Import Seed", command=on_import_seed).pack(side=tk.LEFT, padx=(8, 0))
    show_seed_btn = ttk.Button(btns, text="Show Seed")
    show_seed_btn.pack(side=tk.LEFT, padx=(8, 0))
    root_fingerprint_entry = ttk.Entry(btns, textvariable=root_fingerprint_var, width=28, state="readonly")
    root_fingerprint_entry.pack(side=tk.LEFT, padx=(8, 0))

    def open_settings() -> None:
        existing = settings_window.get("window")
        if existing is not None and existing.winfo_exists():
            existing.lift()
            existing.focus_set()
            return

        win = tk.Toplevel(root)
        win.title("Settings")
        win.resizable(False, False)
        win.transient(root)
        win.protocol("WM_DELETE_WINDOW", win.destroy)

        panel = ttk.Frame(win, padding=14)
        panel.pack(fill=tk.BOTH, expand=True)
        ttk.Label(panel, text="Settings", font=bold_font).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
        ttk.Label(panel, text="Dark Mode").grid(row=1, column=0, sticky="w", padx=(0, 28))
        ttk.Checkbutton(panel, text="On", variable=dark_mode_var).grid(row=1, column=1, sticky="e")
        ttk.Button(panel, text="Close", command=win.destroy).grid(row=2, column=0, columnspan=2, sticky="e", pady=(14, 0))

        settings_window["window"] = win
        settings_window["frame"] = panel
        apply_dark_mode()
        win.grab_set()
        win.focus_set()

    def apply_dark_mode(*_args) -> None:
        dark = dark_mode_var.get()
        colors = (
            {
                "bg": "#111827",
                "card": "#1f2937",
                "field": "#111827",
                "text": "#f9fafb",
                "muted": "#9ca3af",
                "button": "#374151",
                "border": "#4b5563",
                "select": "#1d4ed8",
            }
            if dark
            else {
                "bg": "#f7f8fa",
                "card": "#ffffff",
                "field": "#ffffff",
                "text": "#111827",
                "muted": "#6b7280",
                "button": "#ffffff",
                "border": "#d1d5db",
                "select": "#dbeafe",
            }
        )
        current_theme["colors"] = colors
        style = ttk.Style(root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", background=colors["bg"], foreground=colors["text"])
        style.configure("TFrame", background=colors["bg"])
        style.configure("TLabel", background=colors["bg"], foreground=colors["text"])
        style.configure("TButton", background=colors["button"], foreground=colors["text"])
        style.configure("TCheckbutton", background=colors["bg"], foreground=colors["text"])
        style.configure("TRadiobutton", background=colors["bg"], foreground=colors["text"])
        style.configure("TEntry", fieldbackground=colors["field"], foreground=colors["text"])
        style.configure("TCombobox", fieldbackground=colors["field"], foreground=colors["text"])
        root.configure(bg=colors["bg"])
        settings_win = settings_window.get("window")
        if settings_win is not None and settings_win.winfo_exists():
            settings_win.configure(bg=colors["bg"])
        themed_frames = [frm, title_row, seed_len_row, words_frame, btns]
        settings_frame = settings_window.get("frame")
        if settings_frame is not None and settings_frame.winfo_exists():
            themed_frames.append(settings_frame)
        for widget in themed_frames:
            widget.configure(style="TFrame")
        for text_widget in (mnemonic_txt, output):
            text_widget.configure(
                bg=colors["field"],
                fg=colors["text"],
                insertbackground=colors["text"],
                selectbackground=colors["select"],
            )
        copy_seed_btn.configure(
            bg="#dc2626",
            fg="#111827",
            activebackground="#b91c1c",
            activeforeground="#111827",
        )
        generate_seed_btn.configure(
            bg="#22c55e",
            fg="#111827",
            activebackground="#16a34a",
            activeforeground="#111827",
        )
        mnemonic_txt.tag_configure("valid_word", foreground=valid_color, font=bold_font)
        mnemonic_txt.tag_configure("invalid_word", foreground=invalid_color, font=bold_font)
        refresh_numbered_entries_style()
        highlight_main_text_words()

    settings_btn.configure(command=open_settings)
    mnemonic_txt.bind("<KeyRelease>", on_main_text_change)
    mnemonic_txt.bind("<<Modified>>", on_mnemonic_modified)
    for e in word_entries:
        e.bind("<KeyRelease>", on_entry_change)
        e.bind("<FocusOut>", on_entry_change)
    seed_len_var.trace_add("write", lambda *_: on_seed_length_change())
    dark_mode_var.trace_add("write", apply_dark_mode)
    passphrase_var.trace_add("write", refresh_root_fingerprint_display)
    coin_combo.bind("<<ComboboxSelected>>", on_coin_change)
    show_seed_btn.bind("<ButtonPress-1>", reveal_imported_seed)
    show_seed_btn.bind("<ButtonRelease-1>", hide_imported_seed)
    show_seed_btn.bind("<Leave>", hide_imported_seed)

    all_entry_widgets = [*word_entries]
    all_entry_widgets.extend([passphrase_entry, derivation_entry, count_entry])
    for e in all_entry_widgets:
        install_clipboard_bindings(e, is_text_widget=False)
    install_clipboard_bindings(mnemonic_txt, is_text_widget=True)
    install_clipboard_bindings(output, is_text_widget=True)
    install_clipboard_bindings(root_fingerprint_entry, is_text_widget=False)

    on_seed_length_change()
    apply_dark_mode()
    highlight_main_text_words()
    sync_state["last_main_words"] = normalize_mnemonic_words(mnemonic_txt.get("1.0", tk.END).strip())
    mnemonic_txt.edit_modified(False)
    refresh_root_fingerprint_display()

    root.mainloop()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Arculus Recovery")
    p.add_argument("--gui", action="store_true", help="Launch simple desktop GUI.")
    p.add_argument("--mnemonic", help="BIP39 mnemonic (12 or 24 words).")
    p.add_argument("--passphrase", default="", help="Optional BIP39 passphrase.")
    p.add_argument(
        "--derivation",
        default="",
        help="Custom derivation path. Supports both ' and h. Defaults to coin standard (e.g. Litecoin m/84'/2'/0').",
    )
    p.add_argument("--all-common", action="store_true", help="Derive m/44'/coin'/0', m/49'/coin'/0', m/84'/coin'/0', and m/86'/coin'/0'.")
    p.add_argument("--script-type", choices=["auto", "p2pkh", "p2wpkh-p2sh", "p2wpkh", "p2tr"], default="p2wpkh")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--coin", choices=["bitcoin", "litecoin", "dogecoin"], default="bitcoin")
    p.add_argument("--testnet", action="store_true")
    p.add_argument("--output-format", choices=["json", "csv", "txt"], default="json", help="CLI output format.")
    return p


def main() -> None:
    args = build_parser().parse_args()
    if args.gui or not args.mnemonic:
        launch_gui()
        return

    out = run_derivation(
        mnemonic=args.mnemonic,
        passphrase=args.passphrase,
        derivation=args.derivation,
        all_common=args.all_common,
        script_type=args.script_type,
        count=args.count,
        coin=args.coin,
        testnet=args.testnet,
    )
    print(format_derived_output(out, args.output_format), end="")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
