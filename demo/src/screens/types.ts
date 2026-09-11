import type { ComponentType } from 'react'

export interface DemoScreenDefinition {
  readonly component: ComponentType
  readonly description: string
  readonly title: string
}

export type DemoScreenRegistry = Readonly<Record<string, DemoScreenDefinition>>
