#!/usr/bin/env python3
"""
Standalone offline BIP39/BIP32 restore tool with optional Tkinter GUI.
No external dependencies (Python standard library only).
"""

import argparse
import hashlib
import hmac
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
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

MAINNET = {
    "p2pkh": {"xprv": 0x0488ADE4, "xpub": 0x0488B21E},
    "p2wpkh-p2sh": {"xprv": 0x049D7878, "xpub": 0x049D7CB2},
    "p2wpkh": {"xprv": 0x04B2430C, "xpub": 0x04B24746},
    "wif": 0x80,
    "p2pkh_prefix": 0x00,
    "p2sh_prefix": 0x05,
    "hrp": "bc",
}

TESTNET = {
    "p2pkh": {"xprv": 0x04358394, "xpub": 0x043587CF},
    "p2wpkh-p2sh": {"xprv": 0x044A4E28, "xpub": 0x044A5262},
    "p2wpkh": {"xprv": 0x045F18BC, "xpub": 0x045F1CF6},
    "wif": 0xEF,
    "p2pkh_prefix": 0x6F,
    "p2sh_prefix": 0xC4,
    "hrp": "tb",
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


def bip39_to_seed(mnemonic: str, passphrase: str) -> bytes:
    m = normalize_nfkd(" ".join(mnemonic.strip().split()))
    p = normalize_nfkd(passphrase)
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048, dklen=64)


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
    child_k = (int.from_bytes(IL, "big") + node.k) % N
    if child_k == 0:
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


def pubkey_to_address(pubkey: bytes, script_type: str, netcfg: dict) -> str:
    pkh = hash160(pubkey)
    if script_type == "p2pkh":
        return b58check(bytes([netcfg["p2pkh_prefix"]]) + pkh)
    if script_type == "p2wpkh":
        return segwit_addr_v0(netcfg["hrp"], pkh)
    if script_type == "p2wpkh-p2sh":
        redeem = b"\x00\x14" + pkh
        return b58check(bytes([netcfg["p2sh_prefix"]]) + hash160(redeem))
    raise ValueError(f"unsupported script type: {script_type}")


def derive_account(mnemonic: str, passphrase: str, derivation: str, script_type: str, count: int, netcfg: dict):
    seed = bip39_to_seed(mnemonic, passphrase)
    root = master_from_seed(seed)
    account = derive(root, derivation)
    st = purpose_to_script_type(derivation) if script_type == "auto" else script_type
    account_versions = netcfg[st]
    root_versions = netcfg["p2pkh"]

    result = {
        "derivation": derivation,
        "account_script_type_used": st,
        "root_xprv": ext_prv_to_base58(root, root_versions["xprv"]),
        "root_xpub": ext_pub_to_base58(root, root_versions["xpub"]),
        "account_xprv": ext_prv_to_base58(account, account_versions["xprv"]),
        "account_xpub": ext_pub_to_base58(account, account_versions["xpub"]),
        "receiving": [],
        "change": [],
    }

    for branch, key in ((0, "receiving"), (1, "change")):
        branch_node = ckd_priv(account, branch)
        for i in range(count):
            child = ckd_priv(branch_node, i)
            pub = ser_pubkey(child.pub())
            result[key].append(
                {
                    "path": f"{derivation}/{branch}/{i}",
                    "address": pubkey_to_address(pub, st, netcfg),
                    "public_key_hex": pub.hex(),
                    "private_key_hex": ser256(child.k).hex(),
                    "private_key_wif": to_wif(child.k, netcfg),
                }
            )
    return result


def run_derivation(
    mnemonic: str,
    passphrase: str,
    derivation: str,
    all_common: bool,
    script_type: str,
    count: int,
    testnet: bool,
) -> Dict:
    words_ok, checksum_ok, msg = bip39_validate(mnemonic)
    if not words_ok:
        raise ValueError(msg)
    if not checksum_ok:
        raise ValueError(msg)
    if count < 1:
        raise ValueError("--count must be >= 1")

    netcfg = TESTNET if testnet else MAINNET
    derivations = ["m/44'/0'/0'", "m/49'/0'/0'", "m/84'/0'/0'"] if all_common else [derivation]
    derivations = [normalize_path(d) for d in derivations]

    out = {
        "network": "testnet" if testnet else "mainnet",
        "word_count": len(normalize_mnemonic_words(mnemonic)),
        "accounts": [],
    }
    for d in derivations:
        out["accounts"].append(derive_account(mnemonic, passphrase, d, script_type, count, netcfg))
    return out


def launch_gui() -> None:
    import tkinter as tk
    import tkinter.font as tkfont
    from tkinter import filedialog
    from tkinter import ttk
    from tkinter.scrolledtext import ScrolledText

    root = tk.Tk()
    root.title("Arculus BTC Recovery")
    root.geometry("1080x840")

    frm = ttk.Frame(root, padding=10)
    frm.pack(fill=tk.BOTH, expand=True)
    frm.columnconfigure(1, weight=1)
    frm.rowconfigure(10, weight=1)

    normal_font = tkfont.nametofont("TkDefaultFont").copy()
    bold_font = tkfont.nametofont("TkDefaultFont").copy()
    bold_font.configure(weight="bold")
    valid_color = "#1b8f2f"
    invalid_color = "#b71c1c"

    ttk.Label(frm, text="Mnemonic (12 or 24 words):").grid(row=0, column=0, sticky="w")
    mnemonic_txt = ScrolledText(frm, height=4, wrap=tk.WORD)
    mnemonic_txt.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
    mnemonic_txt.tag_configure("valid_word", foreground=valid_color, font=bold_font)
    mnemonic_txt.tag_configure("invalid_word", foreground=invalid_color, font=bold_font)

    seed_len_var = tk.IntVar(value=12)
    seed_len_row = ttk.Frame(frm)
    seed_len_row.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(4, 0))
    ttk.Label(seed_len_row, text="Seed length:").pack(side=tk.LEFT)
    ttk.Radiobutton(seed_len_row, text="12 words", value=12, variable=seed_len_var).pack(side=tk.LEFT, padx=(8, 0))
    ttk.Radiobutton(seed_len_row, text="24 words", value=24, variable=seed_len_var).pack(side=tk.LEFT, padx=(8, 0))

    ttk.Label(frm, text="Numbered Words:").grid(row=2, column=0, sticky="nw")
    words_frame = ttk.Frame(frm)
    words_frame.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=(2, 0))
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

    ttk.Label(frm, text="Passphrase:").grid(row=3, column=0, sticky="w")
    passphrase_var = tk.StringVar()
    passphrase_entry = ttk.Entry(frm, textvariable=passphrase_var, show="*")
    passphrase_entry.grid(row=3, column=1, sticky="ew", padx=(8, 0))

    ttk.Label(frm, text="Derivation:").grid(row=4, column=0, sticky="w")
    derivation_var = tk.StringVar(value="m/0'")
    derivation_entry = ttk.Entry(frm, textvariable=derivation_var)
    derivation_entry.grid(row=4, column=1, sticky="ew", padx=(8, 0))

    ttk.Label(frm, text="Script Type:").grid(row=5, column=0, sticky="w")
    script_label_to_value = {
        "Auto": "auto",
        "P2PKH": "p2pkh",
        "P2WPKH-P2SH": "p2wpkh-p2sh",
        "P2WPKH": "p2wpkh",
    }
    script_var = tk.StringVar(value="P2WPKH")
    ttk.Combobox(frm, textvariable=script_var, values=list(script_label_to_value.keys()), state="readonly").grid(
        row=5, column=1, sticky="w", padx=(8, 0)
    )

    ttk.Label(frm, text="Address Count:").grid(row=6, column=0, sticky="w")
    count_var = tk.StringVar(value="5")
    count_entry = ttk.Entry(frm, textvariable=count_var, width=8)
    count_entry.grid(row=6, column=1, sticky="w", padx=(8, 0))

    status_var = tk.StringVar(value="Ready")
    ttk.Label(frm, textvariable=status_var).grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 6))

    output = ScrolledText(frm, height=20, wrap=tk.NONE)
    output.grid(row=10, column=0, columnspan=2, sticky="nsew")

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

    def on_mnemonic_modified(_event=None) -> None:
        # Handle typing, paste, and programmatic text updates consistently.
        if mnemonic_txt.edit_modified():
            mnemonic_txt.edit_modified(False)
            on_main_text_change()

    sync_guard = {"busy": False}
    sync_state = {"last_main_words": []}

    def style_entry_for_word(entry: tk.Entry, raw_word: str, enabled: bool) -> None:
        if not enabled:
            entry.configure(state="disabled", fg="gray", font=normal_font)
            return
        entry.configure(state="normal")
        word = normalize_nfkd(raw_word.strip().lower())
        if word == "":
            entry.configure(fg="black", font=normal_font)
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

    def on_entry_change(_event=None) -> None:
        if sync_guard["busy"]:
            return
        sync_guard["busy"] = True
        try:
            refresh_numbered_entries_style()
            set_main_text_from_entries()
        finally:
            sync_guard["busy"] = False

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
            set_main_text_from_entries()
            sync_state["last_main_words"] = normalize_mnemonic_words(mnemonic_txt.get("1.0", tk.END).strip())
        finally:
            sync_guard["busy"] = False

    def on_validate() -> None:
        mnemonic = mnemonic_txt.get("1.0", tk.END).strip()
        words_ok, checksum_ok, msg = bip39_validate(mnemonic)
        status_var.set(msg)
        if words_ok and checksum_ok:
            set_output(json.dumps({"validation": "ok", "message": msg}, indent=2))
        else:
            set_output(json.dumps({"validation": "failed", "message": msg}, indent=2))

    def on_derive() -> None:
        try:
            mnemonic = mnemonic_txt.get("1.0", tk.END).strip()
            data = run_derivation(
                mnemonic=mnemonic,
                passphrase=passphrase_var.get(),
                derivation=derivation_var.get().strip(),
                all_common=False,
                script_type=script_label_to_value.get(script_var.get(), "p2wpkh"),
                count=int(count_var.get()),
                testnet=False,
            )
            status_var.set("Derivation complete.")
            set_output(json.dumps(data, indent=2))
        except Exception as e:
            status_var.set(f"Error: {e}")
            set_output(json.dumps({"error": str(e)}, indent=2))

    def on_export() -> None:
        text = output.get("1.0", tk.END).strip()
        if not text:
            status_var.set("Nothing to export. Derive or validate first.")
            return
        path = filedialog.asksaveasfilename(
            title="Export Output",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="Arculus_BTC_Recovery_Output.txt",
        )
        if not path:
            status_var.set("Export canceled.")
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        status_var.set(f"Exported to: {path}")

    btns = ttk.Frame(frm)
    btns.grid(row=9, column=0, columnspan=2, sticky="w", pady=(8, 0))
    ttk.Button(btns, text="Validate Mnemonic", command=on_validate).pack(side=tk.LEFT)
    ttk.Button(btns, text="Derive Keys + Addresses", command=on_derive).pack(side=tk.LEFT, padx=(8, 0))
    ttk.Button(btns, text="Export", command=on_export).pack(side=tk.LEFT, padx=(8, 0))

    mnemonic_txt.bind("<KeyRelease>", on_main_text_change)
    mnemonic_txt.bind("<<Modified>>", on_mnemonic_modified)
    for e in word_entries:
        e.bind("<KeyRelease>", on_entry_change)
        e.bind("<FocusOut>", on_entry_change)
    seed_len_var.trace_add("write", lambda *_: on_seed_length_change())

    all_entry_widgets = [*word_entries]
    all_entry_widgets.extend([passphrase_entry, derivation_entry, count_entry])
    for e in all_entry_widgets:
        install_clipboard_bindings(e, is_text_widget=False)
    install_clipboard_bindings(mnemonic_txt, is_text_widget=True)
    install_clipboard_bindings(output, is_text_widget=True)

    on_seed_length_change()
    highlight_main_text_words()
    sync_state["last_main_words"] = normalize_mnemonic_words(mnemonic_txt.get("1.0", tk.END).strip())
    mnemonic_txt.edit_modified(False)

    root.mainloop()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Standalone offline BIP39 restore and BIP32 derivation tool.")
    p.add_argument("--gui", action="store_true", help="Launch simple desktop GUI.")
    p.add_argument("--mnemonic", help="BIP39 mnemonic (12 or 24 words).")
    p.add_argument("--passphrase", default="", help="Optional BIP39 passphrase.")
    p.add_argument("--derivation", default="m/0'", help="Custom derivation path. Supports both ' and h.")
    p.add_argument("--all-common", action="store_true", help="Derive m/44'/0'/0', m/49'/0'/0', m/84'/0'/0'.")
    p.add_argument("--script-type", choices=["auto", "p2pkh", "p2wpkh-p2sh", "p2wpkh"], default="p2wpkh")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--testnet", action="store_true")
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
        testnet=args.testnet,
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
