from bs4 import BeautifulSoup

import pandas

# Note that id is likely a feedly id
columns = ["url","text","id","dot","title","published","date_raw"]
ns = pandas.DataFrame(columns=columns)

soup = BeautifulSoup(open('ns.html','r').read())
posts = soup.findAll('div',{'class':'entry'})

# post.attrs
#{'class': ['entry', 'read', 'u0', 'density-29'],
# 'data-alternate-link': 'http://neurostars.org/p/4368/',
# 'data-dot': 'first-story',
# 'data-entryid': 'asvvdx865ekZS29zuuNNEfOY/yfHzvvxJ7EvaV1yXyU=_15869dfb941:14c3484:1e99f69f',
# 'data-inlineentryid': 'asvvdx865ekZS29zuuNNEfOY/yfHzvvxJ7EvaV1yXyU=_15869dfb941:14c3484:1e99f69f',
# 'data-navigation': 'inline',
# 'data-title': 'Nipype Mapnode to write to the same destination file after recon-all pipeline',
# 'data-u': '0',
# 'id': 'asvvdx865ekZS29zuuNNEfOY/yfHzvvxJ7EvaV1yXyU=_15869dfb941:14c3484:1e99f69f_main'}

# Likely id is for the blog, maybe contact feedly and ask them for full data?

for post in posts:
    dot = post.attrs['data-dot']
    title = post.attrs['data-title']    
    url = post.attrs['data-alternate-link']
    feedly_id = post.attrs['id']
    post_id = post.attrs['data-entryid']
    text = post.find('div',{"class":"summary"}).text
    neurostars_id = url.split('/')[-2]
    date_raw = post.find('span',{"class":"ago"}).attrs['title']
    published = date_raw.split('--')[0].replace('published:','').strip()
    ns.loc[neurostars_id] = [url,text,post_id,dot,title,published,date_raw]
    
ns.to_csv('ns.tsv',sep='\t',encoding='utf-8')
