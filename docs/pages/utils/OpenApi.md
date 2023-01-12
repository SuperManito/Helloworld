<body><link rel="stylesheet" href="src/css/element-plus.css" /></body>

# :fa-regular fa-plug: 控制面板开放应用程序接口

## 一、接口说明

  服务端已开启 CORS 跨域支持，使用 HTTP Status Code 标识状态  

  - ### 接口基准地址

    `http://127.0.0.1:5678/openApi`

  - ### 需要授权的 API

    API认证统一使用 Token 认证

    !> 需要在 **请求头（Header）** 或 **请求地址参数（URL）** 中使用 `api-token` 字段并提供 `openApiToken` 的值

    - #### 获取 openApiToken 的方法 <!-- {docsify-ignore} -->

      ```bash
      taskctl panel info | grep ApiToken
      ```
      ?> 此 **Token** 初始值为 `88888888` ，每次修改面板登录认证信息都会随机一个新的 `32` 位字符串


  - ### 支持的请求方法

    - `GET（SELECT）` 从服务器取出资源（一项或多项）
    - `POST（CREATE）` 在服务器新建一个资源
    - `PUT（UPDATE）` 在服务器更新资源（客户端提供改变后的完整资源）
    - `PATCH（UPDATE）` 在服务器更新资源（客户端提供改变的属性）
    - `DELETE（DELETE）` 从服务器删除资源
    - `HEAD` 获取资源的元数据
    - `OPTIONS` 获取信息，关于资源的哪些属性是客户端可以改变的

  - ### 通用返回状态说明

    |  状态码   |         含义           | 说明                                            |
    | :------: | :-------------------: | :---------------------------------------------: |
    |  `200`   |          OK           | 请求成功                                         |
    |  `201`   |        CREATED        | 创建成功                                         |
    |  `204`   |        DELETED        | 删除成功                                         |
    |  `400`   |      BAD REQUEST      | 请求的地址不存在或者包含不支持的参数                 |
    |  `401`   |     UNAUTHORIZED      | 未授权                                           |
    |  `403`   |       FORBIDDEN       | 被禁止访问                                       |
    |  `404`   |       NOT FOUND       | 请求的资源不存在                                  |
    |  `422`   |  Unprocesable entity  | [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误 |
    |  `500`   | INTERNAL SERVER ERROR | 内部错误                                         |

  - ### 业务代码说明

    |    状态码     |       含义       |       说明       |
    | :----------: | :--------------: | :-------------: |
    |     `0`      |       fail       |     请求失败     |
    |     `1`      |     success      |     请求成功     |
    | `403`/`4403` | openApi 认证失败  |    token错误    |

  - ### 通用返回内容

    数据返回格式统一使用 JSON

    |  参数名 | 参数说明 |
    | :----: | :-----: |
    |  code  | 业务代码 |
    |  data  | 返回结果 |
    |  msg   | 结果消息 |
    |  desc  | 结果描述 |

***

## 二、内置接口

  - ### 添加/更新账号数据

    - #### Cookie

      - 请求路径：`updateCookie`
      - 请求方法：`POST`

      - 请求参数

        |  参数名  |   参数说明   |   备注   |
        | :-----: | :---------: | :-----: |
        | cookie  | 完整cookie值 | 不能为空 |
        | userMsg |     备注     | 可以为空 |

      - 接口响应示例

        ```json
        {
          code: 1,
          data: 1,
          msg: "success"
        }
        ```
        > [!NOTE|label:参数说明]
        > `msg` 调用接口结果消息内容  
        > `code` 业务代码中的状态码  
        > `data` 表示提交后服务器中现存的 Cookie 数量（整数）

    - #### WSKEY & Cookie 二合一

      - 请求路径：`addOrUpdateAccount`
      - 请求方法：`POST`

      - 请求参数

        |  参数名  |  参数说明   |            备注           |
        | :-----: | :-------: | :-----------------------: |
        |  ptPin  | pt_pin的值 |          不能为空          |
        |  ptKey  | pt_key的值 |  可以为空，如果为空则不更新   |
        |  wsKey  | ws_key的值 |  可以为空，如果为空则不更新   |
        | remarks |  备注内容   | 可以为空，默认为`ptPin`的值  |

        > `ptKey` 和 `wsKey` 至少需要传入其中任意一个参数即账号不能为空

      - 接口响应示例

        ```json
        {
            code: 1,
            data: {
                cookieCount: 1,
                accountCount: 1
            },
            msg: ""
        }
        ```
        > [!NOTE|label:参数说明]
        > `msg` 调用接口结果消息内容  
        > `code` 业务代码中的状态码  
        > `data` **cookieCount** 表示提交后服务器中现存的 Cookie 数量（整数）  
        >ㅤㅤㅤ   **accountCount** 表示提交后服务器中现存的 wskey 数量（整数）

  - ### 删除账号

    - 请求路径：`cookie/delete`
    - 请求方法：`POST`
    - 请求参数

      | 参数名 |        参数说明        |         备注         |
      | :----: | :-----------------: | :------------------: |
      | ptPins | 由pt_pin的值组成的数组 | 例 `["pin1","pin2"]` |

    - 接口响应示例

      ```json
      {
          code: 1,
          data: {
              cookieCount: 1,
              accountCount: 1,
              deleteCount: 1
          },
          msg: ""
      }
      ```
      > [!NOTE|label:参数说明]
      > `msg` 调用接口结果消息内容  
      > `code` 业务代码中的状态码  
      > `data` **cookieCount** 表示提交后服务器中现存的 Cookie 数量（整数）  
      >ㅤㅤㅤ **accountCount** 表示提交后服务器中现存的 wskey 数量（整数）  
      >ㅤㅤㅤ  **deleteCount** 表示此次删除的 Cookie 数量

  - ### 查看账号数量

    - 请求路径：`count`
    - 请求方法：`GET`

    - 接口响应示例

      ```json
      {
          code: 1,
          data: {
              "cookieCount": 1,
              "accountCount": 1
          },
          msg: ""
      }
      ```
      > [!NOTE|label:参数说明]
      > `msg` 调用接口结果消息内容  
      > `code` 业务代码中的状态码  
      > `data` **cookieCount** 表示服务器当前现存的 Cookie 数量（整数）  
      >ㅤㅤㅤ **accountCount** 表示服务器当前现存的 wskey 数量（整数）

***

## 三、用户自定义接口

> [!NOTE|label:接口规范]
> 请求路径需使用 `openApi` 或 `api/extra` 作为开头，后者无需验证接口Token

> [!NOTE|label:使用方法]
> 将您的 **Api** 脚本以 `extra_server.js` 命名并存放在 **config** 目录下，重启面板后生效，注意检测日志确认是否正确加载

  - ##### 可以参考下方的简单示例

    <div>
    <details>

    <summary title="折叠代码块">点击展开/收起代码块</summary>

    ```javascript
    var path = require('path');
    var fs = require('fs');

    var rootPath = process.env.JD_DIR;
    // 到家果园日志文件夹
    var jddjFruitLogDir = path.join(rootPath, 'log/jddj_fruit/');

    /**
     * 获取文件内容
     * @param fileName 文件路径
     * @returns {string}
     */
     function getFileContentByName(fileName) {
      if (fs.existsSync(fileName)) {
        return fs.readFileSync(fileName, 'utf8');
      }
      return '';
    }

    /**
     * 获取目录中最后修改的文件的路径
     * @param dir 目录路径
     * @returns {string} 最新文件路径
     */
    function getLastModifyFilePath(dir) {
      var filePath = '';

      if (fs.existsSync(dir)) {
        var lastmtime = 0;

        var arr = fs.readdirSync(dir);

        arr.forEach(function (item) {
          var fullpath = path.join(dir, item);
          var stats = fs.statSync(fullpath);
          if (stats.isFile()) {
            if (stats.mtimeMs >= lastmtime) {
              filePath = fullpath;
            }
          }
        });
      }
      return filePath;
    }

    // 获取到家果园互助码列表
    function getJddjFruitCodes() {
      const lastLogPath = getLastModifyFilePath(jddjFruitLogDir);
      const lastLogContent = getFileContentByName(lastLogPath);
      const lastLogContentArr = lastLogContent.split('\n');
      const shareCodeLineArr = lastLogContentArr.filter(item => item.match(/到家果园互助码:JD_/g));
      console.log(shareCodeLineArr);
      const shareCodeStr = shareCodeLineArr[0] || '';
      const shareCodeArr = shareCodeStr.replace(/到家果园互助码:/, '').split(',').filter(code => code.includes('JD_'));
      return shareCodeArr;
    }

    // 生成到家果园互助码文本
    function createJddjFruitCodeTxt(page, size) {
      const shareCodeArr = getJddjFruitCodes();
      if (shareCodeArr.length > size * (page -1)) {
        const filtered = shareCodeArr.filter((code, index) => index + 1 > size * (page - 1) && index + 1 <= size * page);
        return filtered.join(',');
      }
      return '';
    }

    function diyServer(app) {
      /**
       * 获取到家果园互助码
       */
      app.get('/api/extra/sharecode/jddj_fruit', function(req, res) {
        const page = req.query.page || '1';
        const size = req.query.size || '5';
        const content = createJddjFruitCodeTxt(Number(page), Number(size));
        console.log(`到家果园互助码: ${content}`);
        res.setHeader("Content-Type", "text/plain");
        res.send(content);
      });
    }
    
    module.exports = diyServer;
    ```

    </details>
    </div>

***

## 四、内置接口可视化

- ### JavaScript 灵活弹出框 <!-- {docsify-ignore} -->

  > 一个基于 [SweetAlert2](https://www.sweetalert2.cn) 定制的交互面板插件，可在前端项目中轻松引入

  - #### 公开版 <!-- {docsify-ignore} -->

    - ##### 示例

      ```html preview
      <div>
        <button onclick="ExtraAPI()">点击此处查看演示</button>
      </div>
      <script type="text/javascript" src="//cdn.jsdelivr.net/npm/sweetalert2@8"></script>
      <script type="text/javascript" src="openApi-h5-popup.js"></script>

      ```

    - ##### 源码

      <div>
      <details>

      <summary>点击展开/收起代码块</summary>

      ```javascript
      /* A Fussion popup of the Extra API (sweetalert2) - 公开版
       * Author：SuperManito
       * Modified: 2022-05-05
       * Website: https://supermanito.github.io/Helloworld
       * 2021-2022 (c) Powered by Helloworld
      */

      // 用户自定义配置：
      let api = ""; // 面板地址
      let apiToken = ""; // 面板接口授权token
      let Accounts_Maximum = 100; // 预设帐号上限，服务器剩余资源为该预设值减去服务器现存账号数量
      let Admin_Code = ""; // 管理员操作口令
      let background_css = "#FFF"; // 自定义弹窗背景(css background 属性)

      function ExtraAPI(){Swal.fire({title:"服务器自助管理面板",background:background_css,html:'<div style="font-size: 2em"><button id="countCookies" >查询空闲资源</button></br><button style="margin: .2em" id="submitAccount" >提交账号</button>&nbsp;&nbsp;<button style="margin: .2em" id="deleteCookie" >删除账号</button></div>',showConfirmButton:false,showCloseButton:true,onBeforeOpen:()=>{const content=Swal.getContent();const $=content.querySelector.bind(content);const ClickcountCookies=$("#countCookies");const ClicksubmitAccount=$("#submitAccount");const ClickdeleteCookie=$("#deleteCookie");ClickcountCookies.addEventListener("click",()=>{countCookies()});ClicksubmitAccount.addEventListener("click",()=>{submitAccount()});ClickdeleteCookie.addEventListener("click",()=>{deleteCookie()})},})}function countCookies(){var path="/openApi/count";var myHeaders=new Headers();myHeaders.append("Content-Type","application/json");myHeaders.append("api-token",apiToken);var requestOptions={method:"GET",redirect:"follow",headers:myHeaders,};fetch(api+path,requestOptions).then((response)=>response.json()).then((data)=>{var code=data.code;if(code===1){var free_passengers=Accounts_Maximum-data.data.cookieCount;Swal.fire({type:"info",title:"当前服务器还有 "+free_passengers+" 个车位",background:background_css,showConfirmButton:false,timer:2500,})}else{Swal.fire({type:"error",title:"查询失败",text:JSON.parse(JSON.stringify(data.msg)),background:background_css,showConfirmButton:true,})}}).catch(()=>{connectFailed()})}async function submitAccount(){Swal.mixin({input:"text",background:background_css,showCancelButton:true,cancelButtonText:"取消",progressSteps:["1","2","3"],}).queue([{title:"您的京东用户名",html:"请输入 pt_pin 的值，注意是账号的用户名不是昵称",background:background_css,confirmButtonText:"下一步",input:"text",inputAttributes:{autocapitalize:"off",},showLoaderOnConfirm:true,preConfirm:async(pt_pin)=>{if(pt_pin==""){Swal.showValidationMessage(`用户名不能为空`)}},allowOutsideClick:()=>!Swal.isLoading(),},{title:"您的账号",width:1070,html:"请输入 pt_key 或 wskey 的其中任意一个值，注意登录后手动注销或更改密码会导致其失效",background:background_css,confirmButtonText:"下一步",input:"text",inputAttributes:{autocapitalize:"off",},showLoaderOnConfirm:true,preConfirm:async(key)=>{if(key==""){Swal.showValidationMessage(`账号不能为空`)}else{var key_type=await detectType(key);if(key_type=="unknown"){Swal.showValidationMessage(`账号格式有误，请验证后重试`)}}},allowOutsideClick:()=>!Swal.isLoading(),},{title:"您的备注",html:"请输入您的称谓以用于管理员进行登记（可以不填）",background:background_css,confirmButtonText:"确认提交",confirmButtonColor:"#28a745",input:"text",},]).then(async(result)=>{if(result.value){var content=result.value.toString();var pt_pin=content.split(",")[0];var key=content.split(",")[1];var remarks=content.split(",")[2];if(pt_pin==""){touchWarning()}else{var key_type=await detectType(key);if(key_type!="unknown"){if(key_type=="pt_key"){submitPtKey(key,pt_pin,remarks)}else if(key_type=="wskey"){submitWSKEY(key,pt_pin,remarks)}}}}})}function submitPtKey(key,pt_pin,remarks){var path="/openApi/updateCookie";var myHeaders=new Headers();myHeaders.append("Content-Type","application/json");myHeaders.append("api-token",apiToken);if(RegExp(/\%/).test(pt_pin)==false){pt_pin=encodeURIComponent(pt_pin)}var raw=JSON.stringify({cookie:"pt_key="+key+";pt_pin="+pt_pin+";",userMsg:remarks,});var requestOptions={method:"POST",headers:myHeaders,body:raw,redirect:"follow",};fetch(api+path,requestOptions).then((response)=>response.json()).then((data)=>{var code=data.code;if(code===1){Swal.fire({type:"success",title:"提交成功",text:"已将您的 pt_key 添加至服务器",showConfirmButton:false,background:background_css,timer:2000,})}else{Swal.fire({type:"error",title:"提交失败",text:JSON.parse(JSON.stringify(data.msg)),background:background_css,showConfirmButton:true,})}}).catch(()=>{connectFailed()})}function submitWSKEY(key,pt_pin,remarks){var path="/openApi/addOrUpdateAccount";var myHeaders=new Headers();myHeaders.append("Content-Type","application/json");myHeaders.append("api-token",apiToken);if(RegExp(/\%/).test(pt_pin)==false){pt_pin=encodeURIComponent(pt_pin)}var raw=JSON.stringify({ptPin:pt_pin,wsKey:key,remarks:remarks,});var requestOptions={method:"POST",headers:myHeaders,body:raw,redirect:"follow",};fetch(api+path,requestOptions).then((response)=>response.json()).then((data)=>{var code=data.code;if(code===1){Swal.fire({type:"success",title:"提交成功",text:"已将您的 wskey 添加至服务器",background:background_css,showConfirmButton:false,timer:2000,})}else{Swal.fire({type:"error",title:"提交失败",text:JSON.parse(JSON.stringify(data.msg)),background:background_css,showConfirmButton:true,})}}).catch(()=>{connectFailed()})}function deleteCookie(){Swal.fire({title:"您的京东用户名",text:"请输入 pt_pin 的值，注意不是昵称是用户名",input:"text",background:background_css,confirmButtonText:"下一步",showCancelButton:true,cancelButtonText:"取消",}).then((result)=>{if(result.value){var pt_pin=result.value;Swal.fire({type:"warning",title:"请输入管理员口令",background:background_css,input:"text",inputAttributes:{autocapitalize:"off",},showCancelButton:true,confirmButtonText:"确认删除",confirmButtonColor:"#dc3545",showLoaderOnConfirm:true,cancelButtonText:"取消",preConfirm:(Password)=>{if(Password==Admin_Code){var path="/openApi/cookie/delete";var myHeaders=new Headers();myHeaders.append("Content-Type","application/json");myHeaders.append("api-token",apiToken);if(RegExp(/\%/).test(pt_pin)==false){pt_pin=encodeURIComponent(pt_pin)}var delete_pin=new Array(pt_pin);var raw=JSON.stringify({ptPins:delete_pin,});var requestOptions={method:"POST",headers:myHeaders,body:raw,redirect:"follow",};fetch(api+path,requestOptions).then((response)=>response.json()).then((data)=>{var code=data.code;if(code===1){if(data.data.deleteCount===1){Swal.fire({type:"success",title:"删除成功",background:background_css,showConfirmButton:false,timer:2000,})}else{Swal.fire({type:"error",title:"账号不存在",background:background_css,showConfirmButton:true,})}}else{Swal.fire({type:"error",title:"删除失败",text:"请联系管理员进行处理",background:background_css,showConfirmButton:true,})}}).catch(()=>{connectFailed()})}else{Swal.showValidationMessage(`认证失败`)}},allowOutsideClick:()=>!Swal.isLoading(),})}else if(result.value==""){touchWarning()}})}async function detectType(key){var type="unknown";var judge_ptkey_length=key.length==75||key.length==83;var judge_wskey_length=key.length==96||key.length==118;var judge_key_type=RegExp(/[^A-Za-z0-9-_]/).test(key);var judge_key_format=RegExp(/^AAJ[a-z].*/).test(key)||RegExp(/^app_openAAJ[a-z].*/).test(key);if(judge_key_format==true&&judge_key_type==false){if(judge_ptkey_length==true){type="pt_key"}else if(judge_wskey_length==true){type="wskey"}}return type}function connectFailed(){if(api==""){Swal.fire({type:"error",title:"请先配置关联服务器",background:background_css,showConfirmButton:true,})}else{Swal.fire({type:"error",title:"未能与关联服务器建立连接",text:"请联系管理员进行处理",background:background_css,showConfirmButton:true,})}}function touchWarning(){Swal.fire({type:"warning",title:"请不要乱点",background:background_css,showConfirmButton:true,confirmButtonText:"好的",})}
      ```
      > 顶部的变量需要自行配置相关信息

      </details>
      </div>

  - #### 专业版（付费资源） <!-- {docsify-ignore} -->

    <button class="el-button el-button--warning" onclick="javascript:window.open('src/public/demo_pro.html')">点击此处查看演示</span></button>

    - ##### 功能对比

      | 功能描述 | 公开版 | 专业版 | 专业增强版 |
      | :-----: | :---: | :---: | :------: |
      | 查询账号数量 | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 删除账号 | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 提交账号（wskey & pt_key） | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 管理员身份验证 | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 基于 SweetAlert2 最新版本编写 | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 更漂亮的UI与交互动画（可定制）| <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 服务器选择菜单（单一操作对象） | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 同步操作至节点服务器（无上限） | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 提交账号无需提供用户名 | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 提交账号支持账号有效性检测 | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 提交账号支持填入更多格式 | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 提交账号支持登记联系方式 | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 提交账号支持展示用户信息 | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 批量操作账号（提交与删除） | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 有限范围内的技术支持 | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |
      | 后续所有更新内容 | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:red;"><i class="fa-solid fa-xmark"></i></span> | <span style="color:green;"><i class="fa-solid fa-check"></i></span> |

    - ##### 定价

      > [!NOTE|label:为什么要定价？]
      > 公开版逻辑简单代码仅有300行左右，专业版的代码已上千行，拒绝白嫖！  
      > 如有需要请联系作者进行购买，闲人勿扰！

      | :fa-solid fa-sack-dollar: | 公开版 | 专业版 | 专业增强版 |
      | :-----: | :---: | :-------: | :------: |
      | **定价** |  免费  | `RMB 20` | `RMB 88` |

      > [!WARNING|label:声明]
      > 不接受以此名义任何方式的捐赠，更不改变项目永久免费的性质，之所以定价是想让付出变得有意义！
