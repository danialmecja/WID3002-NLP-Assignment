import re
import pandas as pd
import numpy as np

def sigmoid(val):
  a = 1 + np.exp(-val)
  return 5/a

facility = {'Asp' : ['design', 'wad', 'clinic', 'ward', 'hospital', 'site', 'website', 'ambiance', 'outside', 'table', 'pharmaceutical', 'complex', 'wheelchair',
                     'unit', 'pharmacy', 'facility', 'dept','system', 'furniture', 'klink', 'loo', 'chair', 'aircon', 'wifi', 'corridor', 'environment', 'department'],
           'Pos' : ['ready', 'operational', 'reputable', 'nice', 'spacious', 'calmer', 'warm', 'systematic', 'gud', 'bagus', 'quality', 'adequate', 'adequately', 'cozy',
                      'accomodating', 'plenty', 'bersih', 'quiet', 'humane', 'clean', 'cleanliness', 'fastest', 'functioning', 'cleaned', 'good', 'hygienic', 'furnished'],
           'Neg' : ['disorganized', 'uncomfortable', 'noise', 'insufficient', 'kurang', 'neglect', 'unpleasant', 'deteriorated', 'bad', 'unsafe', 'teruk', 'neglected',
                      'panas','disgust', 'squat', 'uncleaned']}


cost = {'Asp' : ['value', 'pricing', 'cost', 'financial', 'fee', 'pay', 'price', 'priced', 'paid', 'cash', 'charged', 'charging', 'charge', 'money', 'allocate', 'byr'],
        'Pos' : ['worth', 'affordable', 'gud', 'reasonable', 'moderate', 'moderately', 'ok', 'suitable', 'budget', 'cheaper', 'reasonably', 'enough', 'refunded',
                   'murah', 'afford'],
        'Neg' : ['underpaid', 'squeeze', 'wasted', 'con', 'poor', 'much', 'expensive', 'overcharging', 'overpriced', 'ridiculous', 'costly', 'burden', 'bad', 'teruk',
                   'mahal', 'scammiest']}

service = {'Asp' : ['scheduling', 'counsel', 'dignity', 'etika', 'performance', 'receptionist', 'doct', 'pesakit', 'instruction', 'service', 'certificate', 'talked',
                      'skill', 'technique', 'conversation', 'counsellor', 'protocol', 'availability', 'profession', 'assistant', 'employee', 'consulted', 
                      'pharmaceutical', 'sevices', 'checkup', 'diagnostic', 'treatment', 'discharge', 'ability', 'rehab', 'procedure', 'communication', 'doc', 'help', 
                      'therapy', 'punctuality', 'doctor', 'counselling', 'counseling', 'psychiatrist', 'pychastric', 'reception', 'receptiionist', 'hospitality', 
                      'doktor', 'specialist', 'consulting', 'overall', 'consult', 'psychiatry', 'mentalhealth', 'mental health', 'consultantion', 'shrink'],
           'Pos' : ['properly', 'compassion', 'acceptance', 'pleasantly', 'happier', 'gratitude', 'listen', 'healthy', 'wellness', 'juxtaposed', 'skilled', 'energy', 
                      'graduated', 'encouraged', 'hardworking', 'confident', 'much', 'saved', 'enlightenment', 'secure', 'beloved', 'reputable', 'help', 'fast', 'speedy',
                      'safe', 'empathetic', 'satisfying', 'helpful', 'stable', 'improvement', 'nice', 'appropriate', 'faaasst', 'welcomed', 'pro', 'savvy', 'profesional', 
                      'exceptionally', 'calmer', 'content', 'warm', 'smoothly', 'improving', 'empathise', 'academic', 'systematic', 'gud', 'welcoming', 'convincing', 
                      'expertise', 'assure', 'detailed', 'quick', 'bagus', 'streamline', 'timely', 'observant', 'loving', 'understanding', 'talented', 'satisfactory', 
                      'excelent', 'holistic', 'knowledgeable', 'responsive', 'professionally', 'exceptional', 'sweet', 'reassurance', 'quality', 'diligent', 'ok', 
                      'suitable', 'confidence', 'freindly', 'trusted', 'relaxing', 'helpful', 'humane', 'considerate', 'effective', 'lliberating', 'respectable', 
                      'comprehensive', 'trustworthy', 'kindly', 'helpfull', 'decent', 'perfect', 'confidentiality', 'therapeutic', 'good', 'peramah', 'heaven', 
                      'apreciative', 'satisfied', 'dedication', 'recommended', 'punctual'],
           'Neg' : ['fake', 'stressed', 'scold', 'con', 'ego', 'loudly', 'insane', 'faking', 'beware', 'rude', 'lazy', 'trigerred', 'mad', 'refused', 'hate', 
                      'sarcastic', 'disorganized', 'ridicule', 'overbookings', 'uncomfortable', 'shouting', 'slapped', 'exhausted', 'frustrated', 'bully', 
                      'inconsistent', 'poorly', 'clueless', 'crazy', 'suspicious', 'stupid', 'blabbering', 'rudest', 'unashamedly', 'unpolite', 'disgusted', 
                      'unprofessional', 'totallyridiculous', 'unfruitful', 'dissatisfied', 'snapped', 'worthless', 'neglect', 'ridiculous', 'disinterested', 
                      'threatening', 'humilliation', 'judgemental', 'rudecounterstaff', 'heartless', 'burden', 'dodgy', 'overwhelmed', 'outraged', 
                      'inefficient', 'gaslighting', 'lashed', 'screaming', 'selfish', 'unpreparedness', 'incompetent', 'inompetent', 'impolite', 'bad', 
                      'disrespectful', 'inexperienced', 'rudeness', 'unsafe', 'discriminated', 'teruk', 'fraud', 'offensive', 'fastest', 'doubtful', 'hurtful', 
                      'disappointed', 'neglected', 'inexperience', 'unsatisfying', 'unempathetic', 'ineffective', 'mislead', 'frustrating', 'worrying', 'hell', 
                      'geram', 'fantastic', 'unsatisfactory', 'unhelpful', 'arrogant', 'intimidating', 'disappointment']}

df_reviews = pd.read_csv('https://raw.githubusercontent.com/danmecj/WID3002-NLP-Assignment/main/Preprocessed_Text.csv')

reviews = {}

for i in range(len(df_reviews.index)):
  location = df_reviews.loc[i]
  locality = location['locality']
  name = location['name']
  text = location['Preprocessed']

  if locality not in reviews:
    reviews[locality] = {}

  if name not in reviews[locality]:
    reviews[locality][name] = {'review' : [], 'total_reviews' : 0,
                               'ratings' : {'facilities' : {'positive' : [],
                                                            'negative' : [],
                                                            'score' : [],
                                                            'sigmoid_score' : [],
                                                            'overall_score' : 0},
                                            'services' : {'positive' : [],
                                                          'negative' : [],
                                                          'score' : [],
                                                          'sigmoid_score' : [],
                                                          'overall_score' : 0},
                                            'cost' : {'positive' : [],
                                                      'negative' : [],
                                                      'score' : [],
                                                      'sigmoid_score' : [],
                                                      'overall_score' : 0}}}

for i in range(len(df_reviews.index)):
  location = df_reviews.loc[i]
  locality = location['locality']
  name = location['name']
  text = location['Preprocessed']
  string = ''
  text = []
  for char in location['Preprocessed']:
      check = str(char)
      if re.match(r'[a-zA-Z]',check):
          string += char
            
      if not re.match(r'[a-zA-Z]',check) and len(string) != 0:
          text.append(string)
          string = ''

  reviews[locality][name]['review'].append(text)
  reviews[locality][name]['total_reviews'] += 1

  for category in reviews[locality][name]['ratings']:
    for sub_cat in reviews[locality][name]['ratings'][category]:
      if sub_cat == 'overall_score':
        continue

      
      reviews[locality][name]['ratings'][category][sub_cat].append(0)

check = 6

for locality in reviews:
  for name in reviews[locality]:
    for index in range(len(reviews[locality][name]['review'])):
      hold = reviews[locality][name]['review'][index]
      num = len(hold)

      for word_idx in range(num):
        back = 0 if word_idx < check else word_idx - check
        front = num if num - check < i else i + check

        pre = hold[back : word_idx + 1]
        focus = hold[word_idx]
        post = hold[word_idx : front]

        if focus in facility['Asp']:
          for word in pre:
            if word in facility['Pos']:
              reviews[locality][name]['ratings']['facilities']['positive'][index] += 1
            if word in facility['Neg']:
              reviews[locality][name]['ratings']['facilities']['negative'][index] += 1

          for word in post:
            if word in facility['Pos']:
              reviews[locality][name]['ratings']['facilities']['positive'][index] += 1
            if word in facility['Neg']:
              reviews[locality][name]['ratings']['facilities']['negative'][index] += 1


        if focus in cost['Asp']:
          for word in pre:
            if word in cost['Pos']:
                reviews[locality][name]['ratings']['cost']['positive'][index] += 1
            if word in cost['Neg']:
                reviews[locality][name]['ratings']['cost']['negative'][index] += 1

          for word in post:
            if word in cost['Pos']:
                reviews[locality][name]['ratings']['cost']['positive'][index] += 1
            if word in cost['Neg']:
                reviews[locality][name]['ratings']['cost']['negative'][index] += 1

        if focus in service['Asp']:
          for word in pre:
            if word in service['Pos']:
                reviews[locality][name]['ratings']['services']['positive'][index] += 1
            if word in service['Neg']:
                reviews[locality][name]['ratings']['services']['negative'][index] += 1

          for word in post:
            if word in service['Pos']:
                reviews[locality][name]['ratings']['services']['positive'][index] += 1
            if word in service['Neg']:
                reviews[locality][name]['ratings']['services']['negative'][index] += 1

        if focus in facility['Neg']:
          reviews[locality][name]['ratings']['facilities']['negative'][index] += 1

        if focus in cost['Neg']:
          reviews[locality][name]['ratings']['cost']['negative'][index] += 1

        if focus in service['Neg']:
          reviews[locality][name]['ratings']['services']['negative'][index] += 1

        if focus in facility['Pos']:
          reviews[locality][name]['ratings']['facilities']['positive'][index] += 1

        if focus in cost['Pos']:
          reviews[locality][name]['ratings']['cost']['positive'][index] += 1

        if focus in service['Pos']:
          reviews[locality][name]['ratings']['services']['positive'][index] += 1

      for c in reviews[locality][name]['ratings']:
        pos = reviews[locality][name]['ratings'][c]['positive'][index]
        neg = reviews[locality][name]['ratings'][c]['negative'][index]
        val = pos/ (neg + 1) if pos >= neg else (neg / (pos + 1)) * -1
        reviews[locality][name]['ratings'][c]['score'][index] = val
        reviews[locality][name]['ratings'][c]['sigmoid_score'][index] = sigmoid(val)

      for c in reviews[locality][name]['ratings']:
        summation = sum(reviews[locality][name]['ratings'][c]['sigmoid_score'])
        length = len(reviews[locality][name]['ratings'][c]['sigmoid_score'])
        reviews[locality][name]['ratings'][c]['overall_score'] = summation / length

overall_score_data = {'name' : [],'locality' : [],
                      'total_reviews' : [],
                      'overall_service_score' : [],
                      'overall_facility_score' : [],
                      'overall_cost_score' : []}

for locality in reviews:
  for name in reviews[locality]:
    overall_score_data['name'].append(name)
    overall_score_data['locality'].append(locality)

    overall_score_data['total_reviews'].append(reviews[locality][name]['total_reviews'])

    hold = reviews[locality][name]['ratings']
    overall_score_data['overall_service_score'].append(hold['services']['overall_score'])
    overall_score_data['overall_facility_score'].append(hold['facilities']['overall_score'])
    overall_score_data['overall_cost_score'].append(hold['cost']['overall_score'])

df_score = pd.DataFrame(data = overall_score_data)

df_score.to_csv('Overall_Category_Score.csv')
df_score.to_excel('Overall_Category_Score.xlsx')

df_score