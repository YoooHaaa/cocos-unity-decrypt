


var filenum = 1;

function file_createdir(pkgname) {
    var mkdirPtr = Module.getExportByName('libc.so', 'mkdir');
    var mkdir = new NativeFunction(mkdirPtr, 'int', ['pointer', 'int']);
    mkdir(Memory.allocUtf8String("/data/data/" + pkgname + "/dump"), 0x0FFF)
    console.log("[+] 初始化dump目录：/data/data/" + pkgname + "/dump");
}

function hook_cocos_js_inflateMemory(funcname, pkgname){
    console.log("[+] hook ", funcname);
    var cocosbase = Module.findExportByName("libcocos2djs.so", funcname);
    if (cocosbase){
        Interceptor.attach(cocosbase, {
            onEnter: function (args) {
                this.buff = args[2];
                if (Process.arch == "arm64"){
                    this.filename = ptr(args[2]).add(0x3d).readCString() + ".js"
                }else{
                    this.filename = filenum + '.js';
                    filenum = filenum + 1;
                }
            },
            onLeave:function (retval) {
                dump_file_write(this.filename, ptr(Memory.readPointer(this.buff)).readCString(), pkgname);
            }
        });
    }
}

function hook_so_js(pkgname) {
    var exports = Process.findModuleByName("libcocos2djs.so").enumerateExports();
    for (var m = 0; m < exports.length; m++) {
        if (exports[m].name.indexOf("inflateMemory") != -1 && exports[m].name.indexOf("inflateMemoryWithHint") == -1) {
            hook_cocos_js_inflateMemory(exports[m].name, pkgname)
            break;
        }
    }
}

function dump_file_write(file_name, file_str, pkgname) {
    var file_path = "/data/data/" + pkgname + "/dump/" + file_name;
    var fd = new File(file_path, "a");
    if (fd && fd != null) {
        fd.write(file_str + "\r\n");
        fd.flush();
        fd.close();
        console.log("[+] write " + file_path +" done:");
    }
}


function hook_so_luac(pkgname){
    var cocosbase = Module.findExportByName("libcocos2dlua.so", "luaL_loadbuffer");
    if (cocosbase){
        Interceptor.attach(cocosbase, {
            onEnter: function (args) {
                var filename = args[3].readCString();
                if (filename.length < 260){
                    var paths = args[3].readCString().split("/");
                    filename = paths[0];
                    for (var i = 1; i < paths.length; i++){
                        filename = filename + "_" + paths[i];
                    }
                    dump_file_write(filename, args[1].readCString(parseInt(args[2])), pkgname); 
                }
            },
            onLeave:function (retval) {
            }
        });
    }
}


function hook_so_sluac(pkgname){
    var cocosbase = Module.findExportByName("libslua.so", "luaL_loadbufferx");
    if (cocosbase){
        Interceptor.attach(cocosbase, {
            onEnter: function (args) {
                var names = args[3].readCString().split("/");
                var luaname = names[names.length - 1].replace("@", "");
                if (luaname.indexOf("lua") != -1){
                    dump_file_write(luaname, args[1].readCString(), pkgname);
                }
                // dump_file_write(filenum + '.lua', args[1].readCString(), pkgname)
                // filenum = filenum  + 1;
            },
            onLeave:function (retval) {
            }
        });
    }
}


function hook_so(pkgname){
    file_createdir(pkgname);
    var android_dlopen_ext = Module.findExportByName(null,"android_dlopen_ext");
    if(android_dlopen_ext!=null){
        Interceptor.attach(android_dlopen_ext,{
            onEnter: function(args){
                var soName = args[0].readCString();
                if(soName.indexOf("libcocos2djs.so") != -1){
                    this.jshook = true;
                }
                else if(soName.indexOf("libcocos2dlua.so") != -1){
                    this.luahook = true;
                }
                else if(soName.indexOf("libslua.so") != -1){
                    this.sluahook = true;
                }
            },
            onLeave:function(retval){
                if(this.jshook){
                    hook_so_js(pkgname);
                }
                else if(this.luahook){
                    hook_so_luac(pkgname);
                }
                else if(this.sluahook){
                    hook_so_sluac(pkgname);
                }
            }
        });
    }
}

rpc.exports = {
    decryptcocos: function decryptcocos(pkgname) {
        hook_so(pkgname);
    }
};




