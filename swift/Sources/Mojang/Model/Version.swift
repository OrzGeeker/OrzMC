//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/25.
//

import Foundation
import JokerKits

public struct Version: Codable {
    
    public let id: String
    public let type: String
    let url: URL?
    let time: String
    let releaseTime: String
    
    public var gameInfo: GameInfo? {
        get async throws {
            guard let data = try await self.url?.getData
            else {
                return nil
            }
            return try JokerKits.JSON.decoder.decode(GameInfo.self, from: data)
        }
    }
}
