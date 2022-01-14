//
//  File.swift
//  
//
//  Created by joker on 2022/1/9.
//
import Foundation
import JokerKits
import Mojang


extension Launcher {
    
    /// 授权验证
    func authenticate() async throws {
        
        guard let accountName = clientInfo.accountName, let accountPassword = self.clientInfo.accountPassword
        else {
            return
        }
        
        let authParam =  Mojang.AuthAPI.AuthReqParam.init(
            agent: Mojang.AuthAPI.AuthReqParam.Agent(),
            username: accountName,
            password: accountPassword
        )
        guard let data = try await Mojang.AuthAPI.authenticate(reqParam: authParam).data
        else {
            return
        }
        
        let authResp = try JSONDecoder().decode(Mojang.AuthAPI.AuthRespone.self, from: data)
        self.clientInfo.clientToken = authResp.clientToken
        self.clientInfo.accessToken = authResp.accessToken
        Platform.console.output("验证账号密码为正版用户", style: .success)
    }
}
