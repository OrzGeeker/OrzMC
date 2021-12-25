//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation

public struct Version: Codable {
    
    let id: String
    let type: String
    let url: URL?
    let time: String
    let releaseTime: String
    
    public var gameInfo: GameInfo? {
        get async throws {
            guard let data = try await data(with: self.url)
            else {
                return nil
            }
            return try Mojang.jsonDecoder.decode(GameInfo.self, from: data)
        }
    }
}
