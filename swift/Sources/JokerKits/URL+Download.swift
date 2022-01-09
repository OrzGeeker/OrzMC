//
//  File.swift
//  
//
//  Created by wangzhizhou on 2021/12/26.
//

import Foundation
import Crypto

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
    var fileSHA1Value: String {
        get throws {
            guard self.isFileURL
            else {
                throw URLError(.badURL)
            }
            
            let data = try Data(contentsOf: self)
            let digest = Insecure.SHA1.hash(data: data)
            let hexBytes = digest.map { String(format: "%02hhx", $0) }
            return hexBytes.joined()
        }
    }
}
