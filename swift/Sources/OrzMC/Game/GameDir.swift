//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Foundation

enum GameDir {
    
    private static let defaultClientType = "vanilla"
    
    case home
    case minecraft
    case manifest
    case gameVersion(version: String)
    case clientDir(version: String, type: String = defaultClientType)
    case assets(version: String, type: String = defaultClientType)
    case assetsObj(version: String, type: String = defaultClientType, path: String)

    private var pathComponents: [String] {
        switch self {
        case .home:
            return [NSHomeDirectory()]
        case .minecraft:
            return GameDir.home.pathComponents + ["minecraft"]
        case .manifest:
            return GameDir.minecraft.pathComponents + ["manifest"]
        case .gameVersion(let version):
            return GameDir.manifest.pathComponents + [version]
        case .clientDir(let version, let type):
            return GameDir.gameVersion(version: version).pathComponents + ["client", type]
        case .assets(let version, let type):
            return GameDir.clientDir(version: version, type: type).pathComponents + ["assets"]
        case .assetsObj(let version, let type, let path):
            return GameDir.assets(version: version, type: type).pathComponents + ["objects", path]
        }
    }
    
    var dirPath: String {
        return NSString.path(withComponents: self.pathComponents)
    }
    
    func filePath(_ filename: String) -> String {
        return NSString.path(withComponents: self.pathComponents + [filename])
    }
}
