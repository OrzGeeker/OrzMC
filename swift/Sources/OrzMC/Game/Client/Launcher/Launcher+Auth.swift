//
//  File.swift
//  
//
//  Created by joker on 2022/1/9.
//

import Foundation
import Mojang


extension Launcher {
    
    /// 授权验证
    func authenticate() async throws {
        guard let startInfo = self.startInfo else {
            return
        }
        
        guard let accountName = startInfo.accountName, let accountPassword = startInfo.accountPassword
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
        self.startInfo?.clientToken = authResp.clientToken
        self.startInfo?.accessToken = authResp.accessToken
        console.output("验证账号密码为正版用户", style: .success)
    }
}
