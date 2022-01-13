//
//  Launcher.swift
//  
//
//  Created by joker on 2022/1/3.
//

import JokerKits
import Mojang

/// Minecraft 客户端启动器
///
/// [写启动器参考文章](https://wiki.vg/Game_files)
///
/// [启动器Wiki](https://minecraft.fandom.com/zh/wiki/教程/编写启动器)
final class Launcher: Client {
    
    /// 客户端启动器启动参数相关
    var startInfo: LauncherStartInfo?
    
    /// 客户端启动
    func start() async throws {
        
        // 向用户获取启动器相关的参数信息
        self.startInfo = try await userInput()
        
        // 正版验证
        try await self.authenticate()
        
        // 下载启动器启动所需要的文件、资源及依赖
        try await self.download()
        
        // 分析参数并启动客户端
        try await self.launch()
    }
}


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
