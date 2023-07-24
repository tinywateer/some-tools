// Claude AI 2.0 智能问答 API
// Description: claude2 
// forked from https://laf.dev/market/templates/64bd2e096c294a2f97285f7f
//
// 使用方法：https://xxxx.laf.dev/Claude2?content=${question} 或者 https://xxxx.laf.dev/Claude2?content=${question}&parentId=${parentId}
// Cluade_Token 请在环境变量中设置
// 参数：content 问题内容，parentId 会话ID
// 返回：res 回复内容，parentId 会话ID
// 作者：LAF

import cloud from '@lafjs/cloud'


export default async function (ctx: FunctionContext) {
  const question = ctx.query.content
  console.log("提问", question)
  const conversationId = ctx.query.parentId
  console.log("conv", conversationId)

  // 初始化 claude
  const { Claude } = await import('claude-ai')
  const claude = new Claude({
    sessionKey: process.env.Cluade_Token
  });

  await claude.init()

  let conversation, res, parentId;
  if (conversationId) {
    conversation = await claude.getConversation(conversationId);
    res = await conversation.sendMessage(`${question}`);
    parentId = conversation.conversationId;
    console.log("回复", res.completion)

    return { res, parentId }
  } else {
    conversation = await claude.startConversation('Hello Claude!');
    res = await conversation.sendMessage(`${question}`);
    parentId = conversation.conversationId;
    console.log("回复", res.completion)

    return { res, parentId };
  }
}
