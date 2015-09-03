from django_assets import Bundle, register

css = Bundle('bootstrap-3.3.5-dist/css/bootstrap.min.css',
             'css/jquery-ui.min.css',
             'css/jquery-ui.theme.min.css',
             'css/jquery-ui.structure.min.css',
             'css/style.css',
             filters='cssmin',
             output='css_all.css')
register('all_css', css)


js = Bundle('js/jquery-2.1.4.min.js',
            'js/jquery_upload_plugin.js',
            'js/jquery.validate.js',
            'js/jquery.ui.core.js',
            'js/jquery-ui-datepicker.min.js',
            'js/scripts.js',
            filters='jsmin', output='js_all.js')
register('js_all', js)
