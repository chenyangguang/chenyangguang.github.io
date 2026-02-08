/**
 * Custom index generator for language filtering
 */

hexo.extend.generator.register('lang-index', function(locals) {
  const config = this.config;
  const perPage = config.index_generator.per_page;
  const orderBy = config.index_generator.order_by || -date;
  
  const posts = locals.posts.sort(orderBy);
  const languages = config.language || ['zh-CN', 'en'];
  
  const result = [];
  
  // Generate index for each language
  languages.forEach(lang => {
    const path = lang === 'zh-CN' ? '' : `${lang}/`;
    
    // Filter posts by language
    const langPosts = posts.filter(post => {
      const postLang = post.lang || post.language || 'zh-CN';
      if (lang === 'zh-CN') {
        return postLang !== 'en';  // Chinese pages show non-English posts
      }
      return postLang === lang;  // Other languages show matching posts
    });
    
    // Calculate pagination
    const total = Math.ceil(langPosts.length / perPage) || 1;
    
    for (let i = 1; i <= total; i++) {
      const base = path + (i === 1 ? '' : `page/${i}/`);
      result.push({
        path: base + 'index.html',
        data: {
          base: path,
          total: total,
          current: i,
          per_page: perPage,
          posts: langPosts.slice((i - 1) * perPage, i * perPage),
          language: lang
        },
        layout: ['index', 'archive']
      });
    }
  });
  
  return result;
});
