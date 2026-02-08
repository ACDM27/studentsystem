// Node.js global types for browser environment
// This file provides minimal Node.js type definitions to satisfy TypeScript

declare namespace NodeJS {
    interface ProcessEnv {
        readonly NODE_ENV: 'development' | 'production' | 'test'
        [key: string]: string | undefined
    }

    interface Process {
        env: ProcessEnv
    }
}

declare var process: NodeJS.Process

// Buffer type (minimal)
declare class Buffer extends Uint8Array {
    toString(encoding?: string): string
    static from(data: any, encoding?: string): Buffer
}

// Timers
declare function setTimeout(callback: (...args: any[]) => void, ms: number, ...args: any[]): NodeJS.Timeout
declare function clearTimeout(timeoutId: NodeJS.Timeout): void
declare function setInterval(callback: (...args: any[]) => void, ms: number, ...args: any[]): NodeJS.Timeout
declare function clearInterval(intervalId: NodeJS.Timeout): void

declare namespace NodeJS {
    interface Timeout {
        ref(): this
        unref(): this
    }
}
