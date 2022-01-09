//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation
import JokerKits

public struct GameInfo: MojangCodable {
    public let arguments: Argument
    public let assetIndex: AssetIndex
    let assets: String
    let complianceLevel: Int
    public let downloads: Download
    let id: String
    let javaVersion: JavaVersion
    public let libraries: [JavaLibrary]
    public let logging: Logging
    public let mainClass: String
    let minimumLauncherVersion: Int
    let releaseTime: String
    let time: String
    public let type: String
}
