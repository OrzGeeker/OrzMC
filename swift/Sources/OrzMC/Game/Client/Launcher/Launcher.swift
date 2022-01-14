//
//  Launcher.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Mojang

/// Minecraft 客户端启动器
///
/// [写启动器参考文章](https://wiki.vg/Game_files)
///
/// [启动器Wiki](https://minecraft.fandom.com/zh/wiki/教程/编写启动器)
class Launcher: Client {
    
    /// 客户端启动器启动参数相关
    var clientInfo: ClientInfo
    
    init(clientInfo: ClientInfo) {
        self.clientInfo = clientInfo
    }
    
    /// 客户端启动
    func start() async throws {
        
        // 正版验证
        try await self.authenticate()
        
        // 下载启动器启动所需要的文件、资源及依赖
        try await self.download()
        
        // 分析参数并启动客户端
        try await self.launch()
    }
}


struct ClientInfo {
    var version: Version
    var username: String
    var debug: Bool = false
    
    // 正版授权
    var accountName: String?
    var accountPassword: String?
    var accessToken: String?
    var clientToken: String?
}
