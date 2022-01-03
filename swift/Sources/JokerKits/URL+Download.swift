//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/26.
//

import Foundation

public extension URL {
    var getData: Data? {
        get async throws {
            let (data, response) = try await URLSession.shared.data(from: self)
            guard (response as? HTTPURLResponse)?.statusCode == 200
            else {
                return nil
            }
            return data
        }
    }
}
