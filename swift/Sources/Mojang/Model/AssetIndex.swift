//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation
import JokerKits

public struct AssetIndex: MojangCodable {
    public let id: String
    public let sha1: String
    public let url: URL
    let size: Int64
    let totalSize: Int64
    
    public var assetInfo: AssetInfo? {
        get async throws {
            guard let data = try await self.url.getData
            else {
                return nil
            }
            return try JokerKits.JSON.decoder.decode(AssetInfo.self, from: data)
        }
    }
}

public struct AssetInfo: MojangCodable {
    public let objects: [String: AssetObjInfo]
    public struct AssetObjInfo: MojangCodable {
        public let hash: String
        let size: Int64
        
        public func filePath() -> String {
            let filename = hash
            let dirPath = self.dirPath()
            return NSString.path(withComponents: [dirPath, filename])
        }
        
        public func dirPath() -> String {
            let startIndex = hash.startIndex
            let endIndex = hash.index(startIndex, offsetBy: 1)
            let path = String(hash[startIndex...endIndex])
            return NSString.path(withComponents: [path])
        }
    }
}
