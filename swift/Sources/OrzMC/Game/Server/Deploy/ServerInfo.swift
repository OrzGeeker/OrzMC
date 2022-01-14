//
//  File.swift
//  
//
//  Created by wangzhizhou on 2022/1/13.
//

import Foundation

struct ServerInfo {
    let version: String
    let gui: Bool
    let debug: Bool
    
    // JVM启动内存占用参数
    var minMem: String
    var maxMem: String
}
