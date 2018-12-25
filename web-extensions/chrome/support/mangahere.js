function MangaHereUsPlugin() {
}

MangaHereUsPlugin.prototype.parseURL = function(url) {
    var parts = url.split("/").filter(function(s) { return s.length !== 0});

    var name = null;
    var chapter = null;
    var page = null;
    if (parts.length === 2 && parts[0] === 'manga') {
        name = parts[1];
    } else if (parts.length === 1) {
        var urlParts = parts[0].split("-chapter-");
        if (urlParts.length < 2) {
            return null;
        } else if (urlParts.length > 1) {
            name = urlParts[0];
            chapter = urlParts[1];
            page = 1;
        }
        if (window.location.search.length > 0) {
            var parts = window.location.search.split("page=");
            if (parts.length > 1) {
                page = parseInt(parts[1].split('&')[0], 10);
            }
        }
    } else {
        return null;
    }

    return { common: { name, chapter, page }};
}
