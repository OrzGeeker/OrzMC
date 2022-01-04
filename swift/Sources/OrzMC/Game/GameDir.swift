//
//  File.swift
//  
//
//  Created by joker on 2022/1/3.
//

import Foundation
import JokerKits

extension Platform {
    func platformName() -> String {
        switch self {
        case .linux:
            return "linux"
        case .windows:
            return "windows"
        case .macosx:
            return "osx"
        default:
            return "unsupported"
        }
    }
}

enum GameDir {
    
    private static let defaultClientType = "vanilla"
    
    case home
    case minecraft
    case manifest
    case gameVersion(version: String)
    case clientDir(version: String, type: String = defaultClientType)
    case assets(version: String, type: String = defaultClientType)
    case assetsObj(version: String, type: String = defaultClientType, path: String)
    case libraries(version: String, type: String = defaultClientType)
    case libraryObj(version: String, type: String = defaultClientType, path: String)
    case clientVersionDir(version: String, type: String = defaultClientType)
    case clientVersionNativeDir(version: String, type: String = defaultClientType)

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
        case .libraries(let version, let type):
            return GameDir.clientDir(version: version, type: type).pathComponents + ["libraries"]
        case .libraryObj(let version, let type, let path):
            return GameDir.libraries(version: version, type: type).pathComponents + [path]
        case .clientVersionDir(let version, let type):
            return GameDir.clientDir(version: version, type: type).pathComponents + ["versions", version]
        case .clientVersionNativeDir(let version, let type):
            let nativesPlatform = "natives-\(Platform.current().platformName())"
            return GameDir.clientVersionDir(version: version, type: type).pathComponents + [nativesPlatform]
        }
    }
    
    var dirPath: String {
        return NSString.path(withComponents: self.pathComponents)
    }
    
    func filePath(_ filename: String) -> String {
        return NSString.path(withComponents: self.pathComponents + [filename])
    }
}
