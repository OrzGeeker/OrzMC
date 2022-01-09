//
//  File.swift
//  
//
//  Created by joker on 2022/1/4.
//

import Mojang

struct LauncherStartInfo {
    var version: Version
    var username: String
    
    // 正版授权
    var accountName: String?
    var accountPassword: String?
    var accessToken: String?
    var clientToken: String?
    
    // UI相关
    var debug: Bool = false
}
