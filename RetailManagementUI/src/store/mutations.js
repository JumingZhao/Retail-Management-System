
export default {
    // 设置当前用户
    setCurrUser (state, user) {
        state.currUser = user;
    },
    // 当前用户退出登录
    logoutAccount (state) {
        state.currUser = {};
    },
}
