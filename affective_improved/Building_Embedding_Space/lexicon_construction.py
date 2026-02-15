
#1.Joy
##  Serenity--------------------------1
##  Joy/ecstasy-----------------------2
#2.Trust
##  Trust-----------------------------3
##  Admire----------------------------4
##  Acceptance------------------------5
#3.Fear
##  Terror/Fear/Apprehension----------6
#4.Surprise
##  Amazement/surprise----------------7
##  Distraction-----------------------8
#5.Sadness
##  sadness/greif/pensiveness---------9
#6.Disgust
##  Boredom--------------------------10
##  Disgust/loathing-----------------11
#7.Anger
##  Anger/Rage/Annoyance-------------12
#8.Anticipation
##  Anticipation---------------------13
##  Vigilance/Interest---------------14

#seedwords from
# https://www.merriam-webster.com/thesaurus/serenity


senerity = ['peace', 'calm', 'calmed', 'peacefully', 'safe', 'composure', 'secure', 'stable', 'stability', 'resolve', 'hush', 'peaceful', 'calming', 'sanity', 'safety', 'warn', 'quo', 'readiness', 'sober', 'sealed', 'reassure', 'well', 'protect', 'quiet', 'conserve', 'orderly', 'resolved', 'alright', 'declare', 'awareness']+['quiet', 'quieter', 'silent', 'silence', 'quietly', 'stillness', 'solitude', 'calm', 'muted', 'peacefully', 'mood', 'sober', 'dim', 'calmed', 'rest', 'peace', 'passive', 'silently', 'peaceful', 'neutral', 'gone', 'busy', 'avoided', 'avoidance', 'idle', 'solitary']+['stillness', 'still', 'keep', 'silently', 'remained', 'silence', 'keeping', 'keeps', 'remain', 'stay', 'hardly', 'not', 'quietly', 'intently', 'continuously', 'merely', 'silent', 'hold', 'pause', 'outside', 'continually', 'constantly', 'now', 'out', 'within', 'already', 'kept', 'meantime', 'beyond', 'pauses']+['calm', 'calmness', 'hush', 'peace', 'peacefulness']+['placidity', 'quiet', 'quietness', 'quietude', 'repose']+['restfulness', 'sereneness', 'still', 'stillness', 'tranquillity']
joy_ecstasy = ['proper','succeed','happiness', 'bliss', 'joy', 'happily', 'enjoyment', 'glee', 'felicity', 'delight', 'sunshine', 'longevity', 'satisfaction', 'optimism', 'perfection', 'enthusiasm', 'prosperity', 'beautifully', 'success', 'fun', 'glory', 'perfect', 'paradise', 'thrive', 'happy', 'charm', 'perfectly', 'maxim', 'jolly', 'thriving', 'sweets']+['ecstasy', 'glory', 'bliss', 'happiness', 'success', 'joy', 'enjoyment', 'delight', 'epic', 'shining', 'adventure', 'pleasure', 'sunshine', 'paradise', 'celebration', 'glamour', 'enjoy', 'innocence', 'triumph', 'spice', 'immensely', 'entertainment', 'fiesta', 'successes', 'satisfaction', 'enthusiasm', 'glee', 'victor', 'excitement']+['enjoyment', 'delight', 'pleasure', 'enjoy', 'enjoys', 'satisfaction', 'bliss', 'amusement', 'enjoying', 'pleasures', 'joy', 'happiness', 'enjoyed', 'enjoyable', 'enthusiasm', 'fun', 'delightful', 'happily', 'entertaining', 'avid', 'sublime', 'charm', 'leisure', 'beautifully', 'refreshing', 'glad', 'delighted', 'pleased', 'sunshine', 'pleasant']+['glee', 'cheer', 'happiness', 'enjoy', 'goodwill', 'bliss', 'joy', 'happily', 'sunshine', 'optimism', 'upbeat', 'smile', 'celebrate', 'enjoyment', 'appreciate', 'enthusiasm', 'virtue', 'encouragement', 'inspirational', 'hope', 'sunny', 'blessings', 'inspire', 'thrive', 'encourage', 'longevity', 'enjoys', 'desirable', 'promise', 'encouraged']+['satisfaction', 'triumph', 'success', 'perfection', 'glory', 'competence', 'happiness', 'achieve', 'successes', 'achievement', 'maxim', 'victory', 'mastery', 'clarity', 'survival', 'accomplishment', 'rewards', 'accomplish', 'longevity', 'prosperity', 'profit', 'achieving', 'excellence', 'fulfillment', 'enhance', 'simplicity', 'successful', 'enjoyment', 'reward']+['beatitude', 'blessedness', 'bliss', 'blissfulness', 'felicity', 'gladness', 'happiness', 'warm fuzzies']+['elatedness', 'elation', 'exhilaration', 'exultation', 'high', 'intoxication']+['ecstasy', 'euphoria', 'glory']+['delectation', 'delight', 'enjoyment', 'pleasure']+['cheer', 'cheerfulness', 'comfort', 'exuberance', 'gaiety', 'gladsomeness', 'glee', 'gleefulness', 'jocundity', 'jollity', 'joyfulness', 'joyousness', 'jubilance', 'jubilation', 'lightheartedness', 'merriness', 'mirth']+['content', 'contentedness', 'gratification', 'satisfaction', 'triumph']
trust = ['safety','assurance', 'certainty', 'confidence', 'assure', 'assured', 'guarantee', 'guaranteed', 'promise', 'reassure', 'secure', 'guarantees', 'reassured', 'sure', 'confident', 'ensures', 'survival', 'determination', 'ensured', 'securing', 'credibility', 'ensure', 'credible', 'acceptance', 'believe', 'safe', 'ensuring', 'awareness', 'confirmation', 'optimism', 'competence']+['believe', 'trust', 'belief', 'believing', 'believes', 'confidence', 'convince', 'believed', 'believer', 'invest', 'sense', 'promote', 'guarantee', 'assurance', 'trusts', 'maintain', 'awareness', 'promise', 'hope', 'assure', 'declare', 'realize', 'reassure', 'achieve', 'ensure', 'faith', 'breathe', 'fully', 'investing', 'succeed']+['acceptance', 'assurance', 'assuredness', 'certainty', 'certitude']+['conviction', 'positiveness', 'sureness', 'surety']+['credit', 'dependence', 'dependance', 'hope', 'reliance']
admire = ['proper','competence','respect', 'esteem', 'regard', 'acknowledge', 'appreciate', 'virtue', 'dignity', 'relevance', 'merits', 'qualities', 'civic', 'uphold', 'importance', 'favour', 'proper', 'moral', 'sincerity', 'praise', 'interest', 'integrity', 'promote', 'recognise', 'ensure', 'recognize', 'respected', 'ethical', 'maxim', 'utmost', 'preserving', 'acknowledging']+['praise', 'favour', 'compliment', 'rewards', 'endorsement', 'favor', 'toast', 'esteem', 'approval', 'merit', 'maxim', 'honor', 'achieve', 'promote', 'respect', 'virtue', 'merits', 'grin', 'laude', 'acknowledge', 'cheer', 'acclaim', 'praises', 'accolades', 'highly', 'promoting', 'civic', 'contribution', 'popularity', 'praised']+['appreciate', 'consider', 'esteem', 'regard', 'respect']+['acclaim', 'accredit', 'applaud', 'approve', 'commend', 'compliment', 'credit', 'praise', 'favour']
acceptance = ['compliance', 'obedience', 'comply', 'obey', 'adherence', 'accordance', 'adhere', 'enforce', 'enforcement', 'compliant', 'strictly', 'maintaining', 'obeyed', 'proper', 'norms', 'principle', 'obligation', 'monitoring', 'complied', 'behave', 'determination', 'duty', 'neutrality', 'commitments', 'conform', 'ethics', 'ensures', 'declaration', 'enforcing', 'obligations']+['believe', 'agree', 'true', 'believes', 'accept', 'promise', 'acceptance', 'belief', 'believed', 'convince', 'acknowledge', 'commitment', 'assure', 'believer', 'sure', 'declare', 'fulfill', 'adhere', 'promises', 'believing', 'promised', 'resolve', 'firmly', 'achieve', 'admit', 'agreed', 'affirmed', 'recognize', 'universally', 'agrees']+['ok', 'obey', 'correct', 'quo', 'declare', 'proper', 'admit', 'succeed', 'properly', 'fundamental', 'believe', 'stable', 'ensure', 'norm', 'achieve', 'declared', 'prove', 'absolutely', 'maha', 'allow', 'pro', 'clear', 'obvious', 'strictly', 'interpret', 'declaration', 'accomplish', 'right', 'convince', 'duly']+['acquiescence', 'biddability', 'compliance', 'compliancy', 'deference', 'docility', 'obedience', 'submissiveness', 'amenability', 'amiability', 'complaisance', 'good-naturedness', 'obsequiousness', 'servility', 'slavishness', 'subservience', 'subserviency', 'Conformity', 'cooperativeness', 'receptiveness', 'receptivity', 'indulgence', 'capitulation', 'submission', 'surrender', 'affability', 'amicability', 'congeniality', 'cordiality', 'friendliness', 'geniality', 'sociability', 'Compromise', 'appeasement', 'conciliation', 'reconcilement', 'reconciliation', 'capture', 'fall', 'capitulating', 'capitulation', 'cession', 'handover', 'relinquishment', 'rendition', 'submitting']
fear = ['awful','terror', 'fright', 'panic', 'fear', 'danger', 'alarm', 'scare', 'scares', 'fears', 'alarms', 'anxiety', 'apprehension', 'worrying', 'paranoia', 'feared', 'fearing', 'hysteria', 'sneaking', 'trapped', 'worried', 'runaway', 'threatens', 'urgency', 'abduction', 'kidnapping', 'hiding', 'anxiously', 'suspense', 'worry', 'crawling']+['fear', 'fears', 'worry', 'danger', 'fearing', 'anxiety', 'terror', 'feared', 'paranoia', 'panic', 'worrying', 'concern', 'risk', 'dangers', 'dread', 'worried', 'threatens', 'threat', 'vulnerability', 'apprehension', 'alarm', 'alarms', 'doubts', 'scares', 'scare', 'distrust', 'risked', 'threats', 'hiding', 'threatened']+['concern', 'worry', 'fear', 'concerns', 'fears', 'dread', 'hazard', 'threat', 'danger', 'avoidance', 'distrust', 'worries', 'doubt', 'terror', 'dire', 'dangers', 'paranoia', 'threatens', 'threats', 'frown', 'urgency', 'suspicion', 'trouble', 'worrying', 'alarm', 'situation', 'trap', 'scare', 'warning', 'noise']+['threat', 'terrorist', 'menace', 'sabotage', 'etat', 'patrolling', 'terrorism', 'arresting', 'conspiracy', 'interrogation', 'paramilitary', 'arrested', 'robbery', 'terrorists', 'intimidation', 'dea', 'jailed', 'threatens', 'evade', 'theft', 'insurrection', 'insurgency', 'raids', 'reactive', 'assassinate', 'pacing', 'arrests', 'terror', 'illegally', 'paced']+['alarm', 'anxiety', 'dread', 'fearfulness', 'fright', 'horror', 'panic', 'scare', 'terror', 'trepidation']+['Phobia', 'creeps', 'jitters', 'nervousness', 'willies', 'fear']+['pang', 'qualm', 'twinge', 'concern', 'dismay', 'worry', 'fear']+['agitation', 'apprehension', 'consternation', 'discomposure', 'disquiet', 'funk', 'perturbation']+['cowardice', 'faintheartedness', 'timidity', 'timorousness']
amazement_surprise = ['astonishment', 'amazement', 'astonishing', 'astonished', 'startling', 'dazed', 'stunned', 'surprising', 'surprise', 'amazing', 'shock', 'shocked', 'amazed', 'surprised', 'peculiar', 'overwhelmed', 'wonder', 'wow', 'unbelievable', 'bizarre', 'curious', 'uncanny', 'impressed', 'fascinating', 'weird', 'intrigued', 'gasped', 'strange', 'unexpected', 'wonders']+['wonder', 'awe', 'surprise', 'wow', 'wonders', 'unbelievable', 'amazement', 'thrilling', 'incredible', 'astonishment', 'amazing', 'amazingly', 'surprises', 'impress', 'astonishing', 'surprising', 'miracle', 'startling', 'marvelous', 'curiosity', 'remarkable', 'sensation', 'unexpected', 'spectacular', 'excitement', 'extraordinary', 'interesting', 'stunning', 'dazed', 'fascinating']+['amazement', 'astonishment', 'shock', 'startlement', 'stupefaction']+['awe', 'wonder', 'wonderment', 'Startle']
distraction = ['confusion', 'distract', 'confuse', 'commotion', 'confusing', 'interference', 'distraction', 'frowning', 'inadvertently', 'interfere', 'scare', 'mistaken', 'skirmish', 'mistakenly', 'evade', 'frown', 'frowns', 'scramble', 'misunderstanding','ambiguity', 'frowned', 'tension', 'threat', 'furrowed']+['maze', 'fog', 'distract', 'haze', 'clouded', 'obstacle', 'evade', 'avoidance', 'tangled', 'trap', 'mist', 'obscured', 'diversion', 'blocking', 'framing', 'avoiding', 'camouflage', 'ditch', 'disguise', 'mole', 'traps', 'moat', 'tangle']+['confuse', 'distract', 'tangled', 'tangle', 'scare', 'furrowed', 'confusion', 'scooted', 'delaying', 'frowns', 'scramble', 'hesitate', 'twitching', 'clouded', 'twitched', 'stemming', 'obscured', 'erroneously', 'risking', 'alarms', 'inadvertently']+['bafflement', 'bamboozlement', 'befuddlement', 'bemusement']+['bewilderedness', 'bewilderment', 'confusedness', 'confusion']+['discombobulation', 'fog', 'head-scratching', 'maze']+['muddle', 'mystification', 'perplexity', 'puzzlement', 'tangle', 'whirl']
sadness = ['poorly','trap','sad', 'grief', 'sadness', 'sorrow', 'sadly', 'disappointment', 'mourning', 'loneliness', 'melancholy', 'misery', 'remorse', 'sorry', 'regret', 'neglect', 'despair', 'lame', 'regrets', 'anguish', 'heartbreak', 'broken', 'ashamed', 'lonely', 'hopeless', 'suffering', 'suffer', 'blamed', 'troubled', 'hurts', 'depressed', 'poor']+['grief', 'sorrow', 'mourning', 'sadness', 'anguish', 'sadly', 'suffering', 'melancholy', 'loneliness', 'misery', 'despair', 'heartbreak', 'sad', 'hopeless', 'remorse', 'devastated', 'wept', 'blamed', 'broken', 'neglect', 'suffer', 'lame', 'disappointment', 'tragic', 'lonely', 'troubled', 'regret', 'neglected', 'sorry', 'suffered']+['agony', 'misery', 'pain', 'despair', 'anguish', 'suffer', 'plight', 'hardship', 'terrible', 'worse', 'badly', 'chronic', 'starvation', 'severe', 'hurts', 'hunger', 'suffered', 'severely', 'neglect', 'worsened', 'ruin', 'low', 'suffers', 'famine', 'grief', 'worst', 'dysfunction', 'futile', 'awful', 'ache']+['avoidance', 'discourage', 'worse', 'worst', 'ignore', 'upset', 'excessive', 'mistake', 'excuses', 'distraction', 'bad', 'wrongly', 'recess', 'pain', 'cry', 'moody', 'sighed', 'overly', 'trouble', 'stress', 'heavily', 'causing', 'negatively', 'diffuse', 'blame', 'trough', 'refuse', 'sob']+['avoidance', 'discourage', 'worse', 'thinner', 'worst', 'ignore', 'upset', 'excessive', 'mistake', 'excuses', 'distraction', 'bad', 'wrongly', 'recess', 'pain', 'cry', 'moody', 'sighed', 'overly', 'trouble', 'stress', 'heavily', 'causing', 'negatively', 'diffuse', 'blame', 'trough', 'refuse', 'sob', 'passive']+['melancholia', 'self-pity', 'sad', 'grief']+['anguish', 'dolor', 'grief', 'mourning', 'somberness', 'sorrow', 'woefulness']+['agony', 'distress', 'pain', 'misery', 'woe', 'wretchedness']+['discouragement', 'disheartenment', 'moodiness']+['despair', 'desperation', 'hopelessness', 'self-despair']+['boredom', 'ennui', 'tedium', 'regret', 'rue']+['dismalness', 'drear', 'morbidness', 'moroseness', 'morosity']+['gloom', 'gloominess', 'glumness', 'melancholy', 'miserablenes']+['misery', 'mopes', 'oppression', 'sorrowfulness', 'unhappiness', 'woefulness', 'wretchedness']
boredom = ['evade','brooding', 'stalking', 'preoccupied', 'disturbing', 'frowning', 'stalked', 'desperate', 'frowned', 'feral', 'moaning', 'obsessed', 'uncomfortably', 'panting', 'groaning']+['indifference', 'indifferent', 'disapproval', 'resentment', 'bitterness', 'disdain', 'ignoring', 'disgust', 'apologetic', 'rejection', 'spite', 'disregard', 'arrogance', 'dislike', 'dissatisfaction', 'ignores', 'disliked', 'hatred', 'irritation', 'frustration', 'cruelty', 'hate', 'oppressive', 'cynical', 'resented', 'refuse', 'rejects']+['useless', 'worthless', 'wasted', 'meaningless', 'vain', 'ineffective', 'pointless', 'futile', 'pathetic', 'stupid', 'dumb', 'empty', 'misery', 'ruined', 'defective', 'outdated', 'boring', 'ignored', 'miserable', 'disastrous', 'terrible', 'deprived', 'foolish', 'doomed', 'poorly', 'ugly', 'obsolete', 'crushed', 'inadequate', 'dull']+['boring', 'dull', 'miserable', 'pathetic', 'disappointed', 'ugly', 'unhappy', 'vain', 'ignored', 'useless', 'worthless', 'wasted', 'disappointment', 'empty', 'depressed', 'misery', 'shitty', 'meaningless', 'dumb', 'poor', 'unfortunate', 'horrible', 'broke', 'deprived', 'lame', 'sorry', 'unpleasant', 'ruined', 'numb', 'messy']+['annoying', 'bothering', 'irritating', 'irritation', 'annoyance', 'distracting', 'exasperated', 'grumbled', 'annoyed', 'scowled', 'interfering', 'bother', 'complaining', 'cursing', 'frustrated', 'irritated', 'bothered', 'distracted', 'offended', 'pointedly', 'insults', 'glaring', 'pinched', 'scowl', 'insult', 'angrily', 'contentious', 'interrupting', 'impatient', 'aggravated']+['blahs', 'doldrums', 'ennui', 'listless', 'restless', 'tedium', 'weariness']+['apathy', 'indifference', 'unconcern']+['dullness', 'monotonousness', 'monotony', 'sameness']+['languidness', 'languor', 'lassitude', 'lethargy', 'lifelessness', 'torpidity', 'torpor']+['aggravation', 'bedevilment', 'botheration', 'bothering']+['bugging', 'disturbance', 'harassment', 'harrying']+['importunity', 'pestering', 'teasing', 'vexation']+['devilment', 'devilry', 'mischief']+['irritability', 'irritableness', 'peeve', 'perturbation', 'pet', 'pique', 'resentment', 'snappishness', 'trouble']
disgust_loathing = ['frown','frowning','evade','avoidance','nausea', 'vomiting', 'vomit', 'psychotic', 'stench', 'hysteria', 'arson', 'rape', 'horrors', 'poisoning', 'choking', 'dumping', 'monster', 'horrific', 'insanity', 'forced', 'massacre', 'coughing', 'screams', 'murder', 'grimaced', 'stink', 'poison', 'painfully', 'pornography', 'grimace', 'curses', 'torture', 'rash', 'horribly']+['hatred', 'hate', 'disgust', 'disdain', 'resentment', 'bitterly', 'disapproval', 'bitterness', 'spite', 'anger', 'condemning', 'racist', 'hated', 'frustration', 'despised', 'contempt', 'resented', 'insults', 'displeasure', 'sneered', 'rage', 'irritation', 'hates', 'hating', 'bastards', 'selfish', 'annoyance', 'cursing', 'hostility', 'spat']+['disapproval', 'displeasure', 'disdain', 'resentment', 'hatred', 'resented', 'dislike', 'disgust', 'hate', 'bitterness', 'bitterly', 'irritation', 'annoyance', 'spite', 'condemning', 'dissatisfaction', 'insults', 'hostility', 'criticisms', 'hates', 'criticizing', 'complaining', 'despised', 'sneered', 'anger', 'hating', 'harshly', 'contempt', 'cursing', 'jealousy']+['revolt', 'rebellion', 'uprising', 'insurrection', 'rebel']+['distress', 'awful', 'anguish', 'terrible', 'severely', 'suffer', 'suffered', 'plight', 'despair', 'badly', 'severe', 'sickness', 'suffers', 'trauma', 'crippled', 'misery', 'deteriorating', 'ruin', 'mortality', 'hopeless', 'struggling', 'inability', 'traumatic', 'poorly', 'devastation', 'sick', 'deterioration', 'asthma', 'hampered', 'crumbling']+['aversion', 'distaste', 'horror', 'loathing', 'nausea', 'repugnance', 'repulsion', 'revulsion', 'disgust', 'loathing']+['abhorrence', 'abomination', 'antipathy', 'execration', 'hate', 'hatred']+['allergy', 'averseness', 'disapproval', 'disfavor', 'disinclination', 'dislike', 'disliking', 'displeasure']+['gross out', 'nauseate', 'put off', 'repel', 'repulse', 'revolt', 'sicken', 'turn off']+['displease', 'distress', 'disquiet', 'horrify']
anger = ['cynical','criticisms','criticize','insults','severely','anger', 'fury', 'rage', 'aggression', 'temper', 'spat', 'raged', 'angrily', 'raging', 'frustration', 'spitting', 'displeasure', 'angry', 'wrath', 'enraged', 'retaliation', 'cursing', 'glare', 'furious', 'irritation', 'snarl', 'bitch', 'furiously', 'insults', 'hostility', 'hatred', 'annoyance', 'glaring', 'contempt', 'insult']+['mad', 'rage', 'furious', 'spat', 'angry', 'enraged', 'angrily', 'anger', 'spitting', 'temper', 'glaring', 'raged', 'frustrated', 'bitch', 'violent', 'raging', 'fury', 'furiously', 'pissed', 'cursing', 'coldly', 'murderous', 'ferocious', 'insults', 'aggression', 'angered', 'dammit', 'brute', 'provoked', 'outraged']+['rage', 'wrath', 'anger', 'aggression', 'fury', 'frustration', 'anarchy', 'outrage', 'displeasure', 'retaliation', 'domination', 'spit', 'curses', 'raging', 'spitting', 'spat', 'arrogance', 'retribution', 'malicious', 'fists', 'mayhem', 'foul', 'bully', 'malice', 'temper', 'furiously', 'scowl', 'loudly', 'defamation', 'shouting']+['malice', 'spite', 'contempt', 'malicious', 'aggression', 'spit', 'rage', 'retaliation', 'nemesis', 'spat', 'fury', 'anger', 'deadly', 'traitor', 'smirked', 'wrath', 'retribution', 'spitting', 'brute', 'defamation', 'bitch', 'brutality', 'vengeance', 'sarcasm', 'arrogance', 'libel', 'satire', 'displeasure', 'glare', 'irritation']+['resentment', 'jealousy', 'bitterness', 'resented', 'disdain', 'disapproval', 'disgust', 'hatred', 'hostility', 'irritation', 'bitterly', 'anger', 'frustration', 'dissatisfaction', 'jealous', 'spite', 'annoyance', 'insults', 'hate', 'despised', 'envy', 'abusive', 'racist', 'bitter', 'selfish', 'complaining', 'displeasure', 'contempt', 'criticisms', 'cursing']+['envy', 'bitterness', 'disgust', 'jealousy', 'resentment', 'disdain', 'hatred', 'bastards', 'hate', 'ironic', 'frustration', 'whore', 'sarcasm', 'unfair', 'disapproval', 'cynical', 'greasy', 'bored', 'selfish', 'annoyance', 'complaining', 'racist', 'irritation', 'dissatisfaction', 'spite', 'resented', 'bitterly', 'spoiled', 'greed', 'asshole']+['angriness', 'birse', 'choler', 'furor', 'fury']+['indignation', 'irateness', 'ire', 'lividity', 'lividness', 'mad']+['madness', 'mood', 'outrage', 'rage', 'spleen', 'wrath', 'wrathfulness']+['malevolence', 'malice', 'spite', 'vengefulness', 'venom', 'vindictiveness', 'virulence', 'vitriol']+['invidiousness', 'jealousy', 'resentment']+['covetousness', 'enviousness', 'envy']+['begrudge', 'resent']+['envy', 'jaundice', 'jealousy', 'pique', 'resentment']
anticipation =['expect', 'expected', 'expects', 'predict', 'expectation', 'anticipated', 'predicted', 'await', 'expecting', 'hopefully', 'prediction', 'anticipating', 'likely', 'assumed', 'projected', 'happen', 'imminent', 'imagine', 'arrive', 'predictions', 'likelihood', 'emerge', 'predicting', 'tomorrow', 'soon', 'sooner', 'prophecy', 'expectations', 'awaited', 'anticipation']+['prospect', 'expectation', 'expect', 'probable', 'anticipated', 'prospects', 'possibility', 'unlikely', 'predicted', 'imminent', 'expected', 'anticipation', 'certainty', 'likelihood', 'potential', 'possible', 'prediction', 'predict', 'await', 'likely', 'predicting', 'prospective', 'predictions', 'anticipating', 'probability', 'chances', 'hopes', 'awaited', 'intuition', 'uncertainty']+['await', 'hope', 'hopes', 'awaited', 'anticipation', 'hoped', 'promise', 'hopefully', 'expect', 'anticipated', 'impending', 'predict', 'imminent', 'future', 'predicted', 'expected', 'anticipating', 'hoping', 'upcoming', 'expectation', 'horizon', 'pursue', 'prophecy', 'assurance', 'expects', 'awaiting', 'hopeful', 'reassure', 'confidently', 'readiness']+['assume', 'assuming', 'assumed', 'assumes', 'suppose', 'obtain', 'assumption', 'define''assumptions', 'predict', 'expectation', 'assert', 'derive']+['wish', 'wishes', 'wished', 'wishing', 'destiny', 'vita', 'promise', 'hope', 'aspirations', 'hopes', 'promised', 'someday', 'promises','forecast',]+['contemplation', 'expectance', 'expectancy']+['expectation', 'prospect']+['anticipate', 'await', 'hope']+['assume', 'presume', 'presuppose']+['envisage', 'envision', 'foresee']
interest_vigilance = ['disquiet','awareness','alert', 'watch', 'alarm', 'monitoring', 'tracking', 'warning', 'monitor', 'lookout', 'tracker', 'monitored', 'alarms', 'warnings', 'surveillance', 'protection', 'worry', 'watches', 'warn', 'guard', 'patrolling', 'indicator', 'siren', 'danger', 'clock', 'warrant', 'check', 'precautions', 'arrest', 'concern', 'safety', 'warned']+['care', 'interest', 'interests']+['readiness', 'preparation', 'prepared', 'preparations', 'preparing', 'prepare', 'ready', 'underway', 'preparatory', 'planning', 'prepares', 'priority', 'anticipated', 'initiation', 'development', 'expectation', 'prospective']+['alert', 'alertness', 'attentiveness', 'watch', 'watchfulness']+['care', 'carefulness', 'cautiousness', 'chariness', 'heedfulness', 'wariness']+['preparation', 'readiness']

senerity = list(set(senerity))
joy_ecstasy = list(set(joy_ecstasy))
trust = list(set(trust))
admire = list(set(admire))
acceptance = list(set(acceptance))
fear = list(set(fear))
amazement_surprise = list(set(amazement_surprise))
distraction = list(set(distraction))
sadness = list(set(sadness))
boredom = list(set(boredom))
disgust_loathing = list(set(disgust_loathing))
anger = list(set(anger))
anticipation = list(set(anticipation))
interest_vigilance = list(set(interest_vigilance))
emo_dict = {'senerity':senerity,
            'joy_ecstasy':joy_ecstasy,
            'trust':trust,
            'admire':admire,
            'acceptance':acceptance,
            'fear':fear,
            'amazement_surprise':amazement_surprise,
            'distraction':distraction,
            'sadness':sadness,
            'boredom':boredom,
            'disgust_loathing':disgust_loathing,
            'anger':anger,
            'anticipation':anticipation,
            'interest_vigilance':interest_vigilance}
voca_lists = [senerity,joy_ecstasy,trust,admire,acceptance,fear,amazement_surprise,distraction,sadness,boredom,disgust_loathing,anger,anticipation,interest_vigilance]
# for each_vl in voca_lists:
#   print(len(each_vl))


# to_r=[]
# each_key='interest_vigilance'
# current_terms = emo_dict[each_key]
# for each_term in current_terms:
#   for other_key in [i for i in emo_dict.keys() if i!=each_key]:
#     if(each_term in emo_dict[other_key]):
#       print(each_term +' in '+each_key+' also in '+other_key)
#       to_r.append(each_term)

# print('probs',to_r)


to_remove_sere=['secure', 'declare', 'declare', 'safety', 'reassure', 'reassure', 'resolve', 'readiness', 'readiness', 'safe', 'avoidance', 'avoidance', 'avoidance', 'warn', 'awareness', 'mood', 'quo']
to_remove_j_e=probs =  ['excitement', 'appreciate', 'virtue', 'competence', 'hope', 'rewards',  'promise']
to_remove_trust = [ 'promote','survival',  'determination', 'hope',  'succeed', 'awareness', 'acceptance',  'optimism',  'competence', 'convince']
to_remove_admire = [ 'proper',  'interest', 'ensure', 'achieve', 'acknowledge', 'recognize', 'maxim']
to_remove_acceptence = [ 'ensure', 'believer', 'achieve', 'believes', 'succeed', 'belief', 'monitoring', 'proper', 'ensures', 'promised', 'promises', 'accomplish', 'believing', 'believed', 'assure', 'believe', 'quo', 'promise', 'promise', 'promise', 'stable']
to_remove_fear = [ 'trap', 'evade', 'hysteria', 'insurrection', 'patrolling', 'concern', 'worry', 'trouble',  'disquiet', 'avoidance', 'frown']
to_remove_amz = []
to_remove_distractions = [ 'avoidance', 'avoidance', 'avoidance', 'scare', 'frowned', 'trap', 'evade', 'frown', 'frowning', 'threat']
to_remove_sad = ['plight', 'distraction', 'awful',  'severely',  'tedium',  'lame', 'ennui', 'futile', 'avoidance', 'passive',  'severe']
to_remove_boredom = ['glaring', 'insult', 'poor', 'sorry', 'hatred', 'hatred', 'poorly', 'cynical','spite', 'spite', 'disdain', 'disdain', 'disgust', 'disgust', 'tedium', 'perturbation', 'disappointment', 'scowl', 'depressed', 'insults', 'insults', 'disapproval', 'disapproval',  'angrily', 'dissatisfaction', 'dissatisfaction', 'hate', 'hate',  'complaining', 'cursing', 'cursing', 'pique', 'resentment', 'resentment', 'trouble', 'trouble', 'irritation', 'irritation', 'refuse', 'frustration', 'frustration', 'frustrated', 'frowning', 'terrible', 'terrible']
to_remove_disgust_l = ['anger', 'contempt', 'curses', 'plight', 'suffered', 'hatred', 'hatred', 'poorly',
                         'distress', 'selfish', 'severely', 'severely',
                       'suffers', 'despair', 'spite', 'spite',
                       'criticisms', 'hopeless', 'insults', 'insults',
                       'despised', 'hate', 'hate', 'rage', 'complaining', 'complaining', 'ruin',
                       'cursing', 'cursing', 'hostility', 'horror',
                        'disquiet', 'suffer',  'frustration',
                       'frustration']
to_remove_anger = [  'bitterness', 'bitterness', 'resented', 'resented', 'disdain',  'disgust', 'disgust',  'displeasure', 'disapproval', 'disapproval', 'annoyance', 'annoyance', 'dissatisfaction', 'dissatisfaction',
                    'resentment', 'resentment', 'racist', 'jealousy', 'arrogance', 'mood', 'bitterly']

to_remove_anticipation = ['reassure', 'reassure', 'assurance']
to_remove_interest = ['safety', 'patrolling', 'danger', 'anticipated', 'expectation']

for each_kk in emo_dict.keys():
  print(each_kk,len(emo_dict[each_kk]))

emo_dict['senerity'] =list(set(emo_dict['senerity'])-set(to_remove_sere))
emo_dict['joy_ecstasy']=list(set(emo_dict['joy_ecstasy'])-set(to_remove_j_e))
emo_dict['trust']=list(set(emo_dict['trust'])-set(to_remove_trust))
emo_dict['admire']=list(set(emo_dict['admire'])-set(to_remove_admire))
emo_dict['acceptance']=list(set(emo_dict['acceptance'])-set(to_remove_acceptence))
emo_dict['fear']=list(set(emo_dict['fear'])-set(to_remove_fear))
emo_dict['amazement_surprise']=list(set(emo_dict['amazement_surprise'])-set(to_remove_amz))
emo_dict['distraction']=list(set(emo_dict['distraction'])-set(to_remove_distractions))
emo_dict['sadness']=list(set(emo_dict['sadness'])-set(to_remove_sad))
emo_dict['boredom']=list(set(emo_dict['boredom'])-set(to_remove_boredom))
emo_dict['disgust_loathing']=list(set(emo_dict['disgust_loathing'])-set(to_remove_disgust_l))
emo_dict['anger']=list(set(emo_dict['anger'])-set(to_remove_anger))
emo_dict['anticipation']=list(set(emo_dict['anticipation'])-set(to_remove_anticipation))
emo_dict['interest_vigilance']=list(set(emo_dict['interest_vigilance'])-set(to_remove_interest))
print('**')
for each_kk in emo_dict.keys():
  print(each_kk,len(emo_dict[each_kk]))

to_remove_all =to_remove_sere+to_remove_j_e+to_remove_trust+to_remove_admire+to_remove_acceptence+to_remove_fear+to_remove_amz+to_remove_distractions+to_remove_sad+to_remove_boredom+to_remove_disgust_l+to_remove_anger+to_remove_anticipation+to_remove_interest

all_words= []
for each_key in emo_dict.keys():
  all_words.extend(emo_dict[each_key])
print('all',len(all_words))
for each_w in to_remove_all:
  if(each_w not in all_words):
    print(each_w)

a = ['a','b','c']
b= ['a','b']
print(list(set(a)-set(b)))

# from google.colab import drive
# drive.mount('/content/drive')
# !pip install transformers
import numpy
import pandas as pd
import ast
from datetime import datetime
from collections import Counter
import torch
from transformers import AutoTokenizer, AutoModel, BertModel,AutoModelForSequenceClassification
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd
import re               # Obtain expressions
from gensim.models import Word2Vec    #Import gensim Word2Fec
from sklearn.decomposition import PCA #Grab PCA functions
import numpy as np
#Plot helpers
import matplotlib
import matplotlib.pyplot as plt
#Enable matplotlib to be interactive (zoom etc)
import ast
import pandas as pd
import ast
from datetime import datetime
# df = pd.read_csv(r"/content/drive/MyDrive/NLP_notebooks/Emotional_embeddings/mean_pooling_embeddings_emo_bert.csv")
# print(df.head())
# df = df.dropna()
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
dis = cosine_similarity([[1, 0, -1]], [[1,-1, 0]])
# print(dis)


#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask

# tokenizer = AutoTokenizer.from_pretrained(r"E:\Projects\emo_detector_new\go_model_simple")
# model = AutoModel.from_pretrained(r"E:\Projects\emo_detector_new\go_model_simple")
tokenizer = AutoTokenizer.from_pretrained("E:\Projects\emo_detector_new\go_model")
model = AutoModel.from_pretrained(r"E:\Projects\emo_detector_new\go_model")
# tokenizer = AutoTokenizer.from_pretrained("joeddav/distilbert-base-uncased-go-emotions-student")
# model = AutoModel.from_pretrained("joeddav/distilbert-base-uncased-go-emotions-student")

tokens = []
embedding = []
eight_label = []
fteen_label = []
category_mapping = {'senerity':'joy',
            'joy_ecstasy':'joy',
            'trust':'trust',
            'admire':'trust',
            'acceptance':'trust',
            'fear':'fear',
            'amazement_surprise':'surprise',
            'distraction':'surprise',
            'sadness':'sadness',
            'boredom':'disgust',
            'disgust_loathing':'disgust',
            'anger':'anger',
            'anticipation':'anticipation',
            'interest_vigilance':'anticipation'}
# for each_key in emo_dict:
#   words_list = emo_dict[each_key]
#
#   for wd in words_list:
#       print(wd)
#       sentences = [wd]
#       encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors='pt')
#       with torch.no_grad():
#           model_output = model(**encoded_input)
#       sentence_embeddings_raw = mean_pooling(model_output, encoded_input['attention_mask'])
#       sentence_embeddings = sentence_embeddings_raw.tolist()[0]
#       tk = wd
#       emb = sentence_embeddings
#       e_lbl = category_mapping[each_key]
#       ft_lbl = each_key
#       tokens.append(tk)
#       embedding.append(emb)
#       eight_label.append(e_lbl)
#       fteen_label.append(ft_lbl)
#     # print(tk)
#     # print(emb)
#     # print(e_lbl)
#     # print(ft_lbl)
#   #  break
#
#
# out_df = pd.DataFrame()
# out_df['token'] = tokens
# out_df['embedding'] = embedding
# out_df['eight_label'] = eight_label
# out_df['fourteen_label'] = fteen_label
#
# out_df.to_csv(r"E:\Projects\emo_detector_new\vocabs\mean_pooling_emb_goemotions_new_vocab_refined.csv")

path = r"E:\Projects\emo_detector_new\vocabs\lnm_goemo_p_n_j_sad.csv"

voc = pd.read_csv(path)
embs = []
print('voc')
for i,row in voc.iterrows():

    wd = row['token']
    print(wd)
    sentences = [wd]
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors='pt')
    with torch.no_grad():
      model_output = model(**encoded_input)
    sentence_embeddings_raw = mean_pooling(model_output, encoded_input['attention_mask'])
    sentence_embeddings = sentence_embeddings_raw.tolist()[0]
    tk = wd
    emb = sentence_embeddings
    embs.append(emb)
outer = voc
outer['embedding'] = embs

outer.to_csv(r"E:\Projects\emo_detector_new\vocabs\lnm_goemo_p_n_j_s.csv")


