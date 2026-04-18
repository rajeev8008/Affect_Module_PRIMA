import json
with open('outputs_100_yuv.json', 'r') as f:
    raw_outputs = json.load(f)
with open('final_9_clusters_affect.json', 'r') as f:
    cluster_outputs = json.load(f)

for cluster in cluster_outputs:
    cid = cluster['cluster_id']
    summary_text = cluster['raw_text']
    summary_emotions = cluster['dominant_emotions']
    summary_peak_val = max(summary_emotions.values()) if summary_emotions else 0
    summary_peak_name = max(summary_emotions, key=summary_emotions.get) if summary_emotions else 'N/A'
    
    print(f'\n--- Cluster {cid} ---')
    print(f'Summary: {summary_text}')
    print(f'Summary Emotion: {summary_peak_name} ({summary_peak_val:.3f})')
    
    matching_raws = []
    for raw in raw_outputs:
        keywords = [w for w in raw['raw_text'].lower().replace('.', '').split() if len(w) > 4]
        matches = sum(1 for kw in keywords if kw in summary_text.lower())
        if matches >= 2:
            raw_peak_val = max(raw['dominant_emotions'].values())
            raw_peak_name = max(raw['dominant_emotions'], key=raw['dominant_emotions'].get)
            matching_raws.append({'text': raw['raw_text'], 'emotion': f'{raw_peak_name} ({raw_peak_val:.3f})'})
            
    print('Raw Memories:')
    for mr in matching_raws:
        print(f'  - {mr["text"]} | Peak: {mr["emotion"]}')
