int ? = Int;
long ? = Long;
double ? = Double;
string ? = String;

bytes = Bytes;
int256 = Int256;

true#3fedd339 = True;
ipPort#d433ad73 ipv4:int port:int = IpPort;
inputPeerPhotoFileLocationLegacy#27d69997 flags:# big:flags.0?true peer:InputPeer volume_id:long local_id:int = InputFileLocation;

---functions---

test.useConfigSimple = help.ConfigSimple;
test.parseInputAppEvent = InputAppEvent;

invokeWithBusinessConnectionPrefix#dd289f8e connection_id:string = Error;
invokeWithGooglePlayIntegrityPrefix#1df92984 nonce:string token:string = Error;
invokeWithApnsSecretPrefix#0dae54f8 nonce:string secret:string = Error;
invokeWithReCaptchaPrefix#adbb0f94 token:string = Error;
invokeWithReCaptcha#adbb0f94 {X:Type} token:string query:!X = X;
ephemeral.editMessage#cf9c725b flags:# invert_media:flags.5?true welcome:flags.6?true peer:flags.7?InputPeer receiver_id:InputUser id:int message:flags.0?string media:flags.3?InputMedia entities:flags.1?Vector<MessageEntity> reply_markup:flags.2?ReplyMarkup rich_message:flags.4?InputRichMessage = Updates;
