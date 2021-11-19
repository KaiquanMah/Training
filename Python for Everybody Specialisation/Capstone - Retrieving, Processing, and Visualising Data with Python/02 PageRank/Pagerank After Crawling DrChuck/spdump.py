import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

cur.execute('''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url
     FROM Pages JOIN Links ON Pages.id = Links.to_id
     WHERE html IS NOT NULL
     GROUP BY id ORDER BY inbound DESC''')

count = 0
print('Column Headers: COUNT(from_id) AS inbound, old_rank, new_rank, id, url')
for row in cur :
    if count < 50 : print(row)
    count = count + 1

print(count, 'rows.')
cur.close()




'''
Visualise Outputs
#only 96 'Pages' records with 'html' field value not being NULL

Column Headers: COUNT(from_id) AS inbound, old_rank, new_rank, id, url
(73, 1.0, 1.0, 241, 'https://www.instagram.com/coursera')
(66, 5.2590691601140485, 5.286376799848498, 232, 'https://www.coursera.org/articles')
(66, 5.265479416524305, 5.317862831712241, 205, 'https://www.coursera.org/articles/how-long-does-a-masters-degree-take')
(66, 5.2590691601140485, 5.286376799848499, 197, 'https://www.coursera.org/degrees/social-sciences')
(66, 5.265479416524305, 5.317862831712241, 195, 'https://www.coursera.org/degrees/data-analytics')
(59, 4.605223006267897, 4.870635211990323, 186, 'https://www.coursera.org/articles/web-developer')
(49, 3.9727013612462536, 5.379773808584641, 228, 'https://www.coursera.org/about/privacy')
(41, 2.9042489802938727, 5.261263497195856, 174, 'https://www.coursera.org/collections/marketing-skills')
(41, 2.900082313627206, 5.240727888148923, 164, 'https://www.coursera.org/courses?query=full%20stack%20web%20development')
(41, 2.895320408865301, 5.217453854552131, 162, 'https://www.coursera.org/courses?query=english%20speaking')
(41, 2.8898259033707956, 5.190854517613607, 143, 'https://www.coursera.org/professional-certificates/salesforce-sales-operations')
(41, 2.900082313627206, 5.240727888148923, 140, 'https://www.coursera.org/professional-certificates/facebook-social-media-marketing')
(41, 2.900082313627206, 5.240727888148923, 67, 'https://www.coursera.org')
(37, 2.5629028264477185, 4.746215206962574, 138, 'https://www.coursera.org/professional-certificates/ibm-data-engineer')
(25, 2.3408356993883315, 0.13230499774162346, 572, 'https://es.coursera.org/courses?query=hr')
(25, 2.3268496854023173, 0.13051563096061866, 571, 'https://es.coursera.org/courses?query=cybersecurity')
(25, 2.3268496854023173, 0.13051563096061866, 568, 'https://es.coursera.org/courses?query=cursos%20gratis')
(22, 1.9733143318669635, 0.1255146437662655, 557, 'https://es.coursera.org/professional-certificates/gcp-cloud-architect')
(13, 1.1885921096447405, 0.058907661301855256, 757, 'https://es.coursera.org/browse/business')
(11, 0.7496244381693293, 1.5806321248303277, 123, 'https://www.coursera.org/browse/information-technology')
(10, 0.6685346945795858, 1.2324524475794438, 126, 'https://www.coursera.org/browse/personal-development')
(9, 1.1313909774436082, 0.24382922420889003, 402, 'https://coursera.community')
(9, 0.8023616734143046, 0.4928522544660412, 350, 'https://es.coursera.org/professional-certificates/soporte-de-tecnologias-de-informacion-google')
(8, 2.275438596491228, 2.09665255500372, 680, 'https://www.youtube.com')
(8, 1.1313909774436082, 0.24382922420889003, 406, 'http://twitter.com/coursera')
(8, 0.9885338345864655, 0.21305560818495511, 388, 'https://www.coursera.org/business/webcast')
(8, 0.9885338345864655, 0.21305560818495511, 382, 'https://www.coursera.org/business/product-teams/?utm_campaign=website&utm_content=product-teams-collection&utm_medium=coursera&utm_source=enterprise')
(8, 0.9885338345864655, 0.21305560818495511, 378, 'https://www.coursera.org/business/engineering-teams/?utm_campaign=website&utm_content=engineering-teams-collection&utm_medium=coursera&utm_source=enterprise')
(8, 0.9885338345864655, 0.21305560818495511, 376, 'https://www.coursera.org/business/cloud-it-academy/?utm_campaign=website&utm_content=cloud-it-academy&utm_medium=coursera&utm_source=enterprise')
(7, 0.6090175175701488, 0.049480494419273185, 759, 'https://es.coursera.org/browse/data-science')
(7, 2.5254385964912283, 3.180848619852367, 690, 'https://www.youtube.com/about/policies')
(7, 0.8635338345864657, 0.21226182503443553, 363, 'https://coursera.org/business')
(6, 0.5944862155388466, 0.0114942624460394, 11, 'https://www.coursera.org/instructor/drchuck')
(5, 0.37047827903091013, 0.012624119914351629, 1078, 'https://es.coursera.org/degrees/imba')
(5, 1.0754385964912274, 1.568960034123289, 869, 'https://socialimpact.youtube.com')
(5, 0.9421052631578942, 1.412692517825364, 867, 'https://www.youtube.com/creators-for-change')
(4, 0.36975677830940945, 0.013912840839256358, 1070, 'https://es.coursera.org/browse/business/leadership-and-management')
(4, 0.26694292549555665, 0.023484449330875047, 1040, 'https://es.coursera.org/learn/negotiation')
(4, 0.23340742504829146, 0.029019143469446083, 437, 'https://www.coursera.org/learn/conclusao-do-marketing-de-midias-sociais-do-facebook')
(4, 0.2898176814585479, 0.40109188646630195, 322, 'https://www.coursera.org/instructor/dan-kob')
(4, 3.0421052631578944, 3.6287280067837773, 47, 'https://www.sakailms.org/sakai-news')
(3, 0.17127192982456094, 0.45337774999774033, 1376, 'https://www.coursera.org/degrees/unt-online-bachelor-completion')
(3, 0.44210526315789433, 0.4230243964099039, 1362, 'https://support.google.com/youtube/answer/3545195?hl=en')
(3, 0.7421052631578943, 0.5283708330863676, 1358, 'https://socialimpact.youtube.com/how-to')
(3, 0.1815283400809712, 0.013962745345464404, 1124, 'https://es.coursera.org/specializations/excel-mysql')
(3, 0.2421052631578943, 0.008645678357577957, 1013, 'https://es.coursera.org/lecture/gcp-infrastructure-core-services/module-overview-jPfvH')
(3, 0.2441254651780963, 0.019250756048278656, 973, 'https://es.coursera.org/learn/it-security')
(3, 0.19045691150954264, 0.017631698764193467, 709, 'https://es.coursera.org/courses?query=human%20resource%20management')
(3, 0.17543859649122762, 0.028619532092129724, 453, 'https://www.coursera.org/specializations/digital-marketing')
(3, 0.2421052631578943, 0.3803532037400506, 323, 'https://www.coursera.org/facebook')
96 rows.
'''
