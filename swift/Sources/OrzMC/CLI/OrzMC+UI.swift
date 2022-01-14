//
//  OrzMC+UI.swift
//  
//
//  Created by wangzhizhou on 2022/1/14.
//

import JokerKits
import ConsoleKit

extension OrzMC {
    static func userInput(hint: String, completedHint: String? = nil) -> String {
        Platform.console.pushEphemeral()
        Platform.console.output(hint, style: .warning, newLine: false)
        let input = Platform.console.input()
        Platform.console.popEphemeral()
        if let completedHint = completedHint {
            Platform.console.output(completedHint.consoleText(.success) + input.consoleText(.info))
        }
        return input
    }
    
    static func chooseFromList<T>(_ list: [T], display: (T) -> ConsoleText, hint: String, completedHint: String) -> T {
        let choose = Platform.console.choose(hint.consoleText(.warning), from: list, display: display)
        Platform.console.output(completedHint.consoleText(.success) + display(choose).description.consoleText(.info))
        return choose
    }
}
