module.exports = {
    root: true,
    env: {
        node: true
    },
    extends: [
        'plugin:vue/essential',
        '@vue/standard'
    ],
    parserOptions: {
        parser: 'babel-eslint'
    },
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'space-before-function-paren': 0,
        'curly': 0,
        'indent': 0,
        'no-trailing-spaces': 0,
        'space-before-blocks': 0,
        'keyword-spacing': 0,
        'vue/no-unused-vars': 0,
        'vue/multi-word-component-names': 0,
        'no-unused-vars': 0,
        'vue/valid-template-root':0
    }
}