
/* === BASE64 === */
(function (context) {
    var Base64 = context.Base64 = {
        map: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
        encode: function (n) {
            var o = "", i = 0, n = this.utf8.encode(n), m = this.map;
                while (i < n.length) {
                    var i1 = n.charCodeAt(i++), i2 = n.charCodeAt(i++), i3 = n.charCodeAt(i++),
                        e1 = (i1 >> 2), e2 = (((i1 & 3) << 4) | (i2 >> 4)), e3 = (isNaN(i2) ? 64 : ((i2 & 15) << 2) | (i3 >> 6)),
                        e4 = (isNaN(i2) || isNaN(i3)) ? 64 : i3 & 63, o = o + m.charAt(e1) + m.charAt(e2) + m.charAt(e3) + m.charAt(e4);
                } return o;
        },
        decode: function (n) {
            var o = "", i = 0, n = n.replace(/[^A-Za-z0-9\+\/\=]/g, ""), m = this.map, cc = String.fromCharCode;
                while (i < n.length) {
                    var e1 = m.indexOf(n.charAt(i++)), e2 = m.indexOf(n.charAt(i++)),
                        e3 = m.indexOf(n.charAt(i++)), e4 = m.indexOf(n.charAt(i++)),
                        c1 = (e1 << 2) | (e2 >> 4), c2 = ((e2 & 15) << 4) | (e3 >> 2),
                        c3 = ((e3 & 3) << 6) | e4, o = o + (cc(c1) + ((e3 != 64) ? cc(c2) : "")) + (((e4 != 64) ? cc(c3) : ""));
                } return this.utf8.decode(o);
        },
        utf8: {
            encode: function (n) {
                var o = "", i = 0, cc = String.fromCharCode;
                    while (i < n.length) {
                        var c = n.charCodeAt(i++), o = o + ((c < 128) ? cc(c) : ((c > 127) && (c < 2048)) ?
                        (cc((c >> 6) | 192) + cc((c & 63) | 128)) : (cc((c >> 12) | 224) + cc(((c >> 6) & 63) | 128) + cc((c & 63) | 128)));
                    } return o;
            },
            decode: function (n) {
                var o = "", i = 0, c = c1 = c2 = 0, cc = String.fromCharCode;
                    while (i < n.length) {
                        var c = n.charCodeAt(i),
                            o = o + ((c < 128) ? [cc(c), i++][0] : ((c > 191) && (c < 224)) ?
                                [cc(((c & 31) << 6) | ((c2 = n.charCodeAt(i + 1)) & 63)), (i += 2)][0] :
                                [cc(((c & 15) << 12) | (((c2 = n.charCodeAt(i + 1)) & 63) << 6) | ((c3 = n.charCodeAt(i + 2)) & 63)), (i += 3)][0]);
                    } return o;
            }
        }
    }; return Base64;
})(this);
