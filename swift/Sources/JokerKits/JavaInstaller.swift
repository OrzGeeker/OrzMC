//
//  File.swift
//  
//
//  Created by joker on 2022/1/15.
//

import Foundation
import SwiftSoup

public enum JDK {
    case jdk17
    
    var downloadUrl: URL {
        get async throws {
            return URL(fileURLWithPath: ".")
        }
    }
    
    enum JDKError: Error {
        case unsupportOS
        case unsupportArch
    }
}

/// JDK安装
///
/// [Oracle Java Installation Guide](https://docs.oracle.com/en/java/javase/17/install/index.html)
public struct JavaInstaller {
    static public func install(_ jdk: JDK) async throws {
        let url = try await jdk.downloadUrl
        url.lastPathComponent
    }
    
    
    /// 获取当前系统安装的Java版本信息
    /// - Returns: 返回的Java版本信息
    static public func currentJavaVersion() throws -> String {
        return try Shell.run(path: "/usr/bin/env", args: ["java", "--version"])
    }
    
    static public func installedJavaVersions() throws -> [String]? {
        var ret: [String]? = nil
        
        switch Platform.os() {
        case .macosx:
            let javaDir = "/Library/Java/JavaVirtualMachines"
            if let jdks = try FileManager.allSubDir(in: javaDir) {
                ret = jdks.map { NSString.path(withComponents: [javaDir, $0]) }
            }
        default:
            break
        }
        return ret;
    }
}
