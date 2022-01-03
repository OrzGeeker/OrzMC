//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation
import JokerKits

public struct GameInfo: Codable, JsonRepresentable {
    let arguments: Argument
    public let assetIndex: AssetIndex
    let assets: String
    let complianceLevel: Int
    public let downloads: Download
    let id: String
    let javaVersion: JavaVersion
    let libraries: [JavaLibrary]
    let logging: Logging
    let mainClass: String
    let minimumLauncherVersion: Int
    let releaseTime: String
    let time: String
    let type: String
}
