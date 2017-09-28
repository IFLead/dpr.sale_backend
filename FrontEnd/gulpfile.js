var gulp = require('gulp'),
    gutil = require('gulp-util'),
    sass = require('gulp-sass'),
    browserSync = require('browser-sync'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    cleanCSS = require('gulp-clean-css'),
    rename = require('gulp-rename'),
    del = require('del'),
    imagemin = require('gulp-imagemin'),
    cache = require('gulp-cache'),
    autoprefixer = require('gulp-autoprefixer'),
    ftp = require('vinyl-ftp'),
    notify = require("gulp-notify"),
    rsync = require('gulp-rsync');

// Скрипты проекта

gulp.task('common-js', function () {
    return gulp.src([
        'app/js/common.js'
    ])
        .pipe(concat('common.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('app/js'));
});

gulp.task('js', ['common-js'], function () {
    return gulp.src([
        'app/libs/jquery/dist/jquery.min.js',
        'app/libs/semantic/dist/semantic.min.js',
        'app/libs/jquery/dist/newWaterfall.js',
        'app/libs/masked-input/jquery.mask.min.js',
        'app/libs/UniteGallery/js/unitegallery.min.js',
        'app/libs/UniteGallery/themes/default/ug-theme-default.js',
        'app/libs/syo/jquery.syotimer.min.js',
        'app/js/common.min.js' // Всегда в конце
    ])
        .pipe(concat('scripts.min.js'))
        .pipe(uglify()) // Минимизировать весь js (на выбор)
        .pipe(gulp.dest('app/js'))
        .pipe(gulp.dest('../static/js'));
});

gulp.task('browser-sync', function () {
    browserSync({
        server: {
            baseDir: 'app'
        },
        notify: false
        // tunnel: true,
        // tunnel: "projectmane", //Demonstration page: http://projectmane.localtunnel.me
    });
});

gulp.task('sass', function () {
    return gulp.src('app/sass/**/*.sass')
        .pipe(sass({outputStyle: 'expand'}).on("error", notify.onError()))
        .pipe(rename({suffix: '.min', prefix: ''}))
        .pipe(autoprefixer(['last 15 versions']))
        //.pipe(cleanCSS()) // Опционально, закомментировать при отладке
        .pipe(gulp.dest('app/css'))
        .pipe(browserSync.reload({stream: true}));
});

gulp.task('html', function () {
   return gulp.src(['app/*.html','app/.htaccess'])
       .pipe(gulp.dest('../templates'));
});

gulp.task('watch', ['sass', 'js', 'html'], function () {
    gulp.watch('app/sass/**/*.sass', ['sass']);
    gulp.watch(['libs/**/*.js', 'app/js/common.js'], ['js']);
    gulp.watch('app/*.html');
});

gulp.task('imagemin', function () {
    return gulp.src('app/img/**/*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest('../static/img'));
});

gulp.task('build', ['removefiles', 'imagemin', 'sass', 'js'], function () {

    var buildFiles = gulp.src([
        'app/*.html',
        'app/.htaccess',
    ]).pipe(gulp.dest('../templates'));

    var buildCss = gulp.src([
        'app/css/main.min.css',
    ]).pipe(gulp.dest('../static/css'));

    var buildJs = gulp.src([
        'app/js/scripts.min.js',
    ]).pipe(gulp.dest('../static/js'));

    var buildFonts = gulp.src([
        'app/fonts/**/*',
    ]).pipe(gulp.dest('../static/fonts'));

});

gulp.task('deploy', function () {

    var conn = ftp.create({
        host: 'hostname.com',
        user: 'username',
        password: 'userpassword',
        parallel: 10,
        log: gutil.log
    });

    var globs = [
        'dist/**',
        'dist/.htaccess',
    ];
    return gulp.src(globs, {buffer: false})
        .pipe(conn.dest('/path/to/folder/on/server'));

});

gulp.task('rsync', function () {
    return gulp.src('dist/**')
        .pipe(rsync({
            root: 'dist/',
            hostname: 'username@yousite.com',
            destination: 'yousite/public_html/',
            archive: true,
            silent: false,
            compress: true
        }));
});

gulp.task('removefiles', function () {
    return del.sync(['../templates', '../static'],{ force:true});
});
gulp.task('clearcache', function () {
    return cache.clearAll();
});

gulp.task('default', ['watch']);

//DEBUG
// gulp.task('debug-image', function () {
//     return gulp.src('app/img/**/*')
//         .pipe(gulp.dest('../static/img'));
// });

// gulp.task('debug-js', ['common-js'], function () {
//     return gulp.src([
//         'app/libs/jquery/dist/jquery.min.js',
//         'app/libs/semantic/dist/semantic.min.js',
//         'app/libs/jquery/dist/newWaterfall.js',
//         'app/libs/masked-input/jquery.mask.min.js',
//         'app/libs/UniteGallery/js/unitegallery.min.js',
//         'app/libs/UniteGallery/themes/default/ug-theme-default.js',
//         'app/libs/syo/jquery.syotimer.min.js',
//         'app/js/common.min.js' // Всегда в конце
//     ])
//         .pipe(concat('scripts.min.js'))
//         .pipe(gulp.dest('app/js'));
// });

// gulp.task('debug', ['removefiles', 'debug-image', 'sass', 'debug-js'], function () {
//
//     var buildFiles = gulp.src([
//         'app/*.html',
//         'app/.htaccess',
//     ]).pipe(gulp.dest('../templates'));
//
//     var buildCss = gulp.src([
//         'app/css/main.min.css',
//     ]).pipe(gulp.dest('../static/css'));
//
//     var buildJs = gulp.src([
//         'app/js/scripts.min.js',
//     ]).pipe(gulp.dest('../static/js'));
//
//     var buildFonts = gulp.src([
//         'app/fonts/**/*',
//     ]).pipe(gulp.dest('../static/fonts'));
//
// });
