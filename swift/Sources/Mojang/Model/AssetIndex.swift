//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation
import JokerKits

public struct AssetIndex: Codable {
    let id: String
    let sha1: String
    let size: Int64
    let totalSize: Int64
    let url: URL
    
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

public struct AssetInfo: Codable, JsonRepresentable {
    public let objects: [String: AssetObjInfo]
    public struct AssetObjInfo: Codable {
        public let hash: String
        let size: Int64
        
        public func path() -> String {
            let startIndex = hash.startIndex
            let endIndex = hash.index(startIndex, offsetBy: 1)
            let path = String(hash[startIndex...endIndex])
            let filename = hash
            return NSString.path(withComponents: [path, filename])
        }
    }
}
