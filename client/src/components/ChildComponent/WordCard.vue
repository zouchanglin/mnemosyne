<template>
    <div>
        <van-popup v-model="show" position="bottom"
                   :style="{ height: height }"
                   round
                   @close="close_word_card"
                   style="text-align: center; background: #fafafa">
            <van-row style="text-align: left; padding-top: 20px" v-if="word_detail.word !== ''" >
                <van-col span="3"></van-col>
                <van-col span="13">
                    <span style="font-size: 22px">{{ word_detail.word }}</span>&nbsp;&nbsp;
                    <span style="font-size: 12px; color: #525252">/{{ word_detail.usphone }}/</span>
                    <br><br>
                    <span style="font-size: 14px; color: #505050;">{{ word_detail.trans }}</span>
                </van-col>
                <van-col span="3">
                    <van-button plain type="primary" @click="click_voice">
                        <van-icon name="volume-o"/>
                    </van-button>
                </van-col>
                <van-col span="3">
                    <van-button plain type="info">
                        <van-icon name="more-o" @click="get_vector_word"/>
                    </van-button>
                </van-col>
                <van-col span="2"></van-col>
            </van-row>

            <van-row style="text-align: left; padding: 20px;" v-if="vector_link_words.length > 0">
                <van-col span="24">
                    <van-cell-group inset style="overflow: auto; height: 50vh; padding: 0">
                        <van-cell v-for="w in vector_link_words" :key="w.id" :title="w.word" :label="w.trans" />
                    </van-cell-group>
                </van-col>
            </van-row>

            <van-row class="fixed-bottom">
                <van-grid style="width: 100%">
                    <van-grid-item v-if="word_detail.learned" icon="completed-o" text="学过"/>
                    <van-grid-item v-if="word_detail.killed" icon="passed" text="已斩"/>
                    <van-grid-item icon="close" :text="'错' + word_detail.error_count + '次'"/>
                    <van-grid-item icon="fire-o" :text="'引用' + word_detail.pitch_count + '次'"/>
                </van-grid>
            </van-row>
        </van-popup>
    </div>
</template>

<script>
import { Toast } from 'vant'

export default {
    name: 'WordCard',
    setup() {

    },
    data() {
        return {
            show: false,
            audio: new Audio(),
            word_detail: {
                word: '',
                error_count: 0,
                pitch_count: 0,
                learned: false,
                killed: false,
                usphone: '',
                trans: ''
            },
            height: '28%',
            vector_words_height: '0px',
            // 向量关联词
            vector_link_words: []
        }
    },
    created() {
        this.audio.autoplay = true
    },
    watch: {
        word_id(newVal) {
            if(newVal === -1){
                return
            }
            this.get_word_detail(newVal)
            this.show = true
        }
    },
    methods: {
        async get_vector_word() {
            console.log('get_vector_word')
            this.height = '75%'
            this.vector_words_height = '50px'
            // 只搜索这一个
            const params = {
                word_ids: [this.word_id],
                search_limit: 15
            }
            const { data: ret } = await this.$http.post('/vector/search', params)
            if (ret.code !== 0) {
                Toast.fail(ret.msg)
                return
            }
            // console.log('vector->', ret.data)
            // 展示出关联词
            this.vector_link_words = ret.data
        },
        close_word_card() {
            this.height = '28%'
            this.$emit('close_word_card')
            this.vector_link_words = []
            this.vector_words_height = '0px'
            this.word_detail.word = ''
        },
        async get_word_detail(id) {
            const params = { id: id }
            const { data: ret } = await this.$http.post('/word/detail', params)
            if (ret.code !== 0) {
                Toast.fail(ret.msg)
                return
            }
            console.log('detail->', ret.data)
            // 展示单词详情页
            this.word_detail = ret.data
            if (ret.data.usspeech.length === 0) {
                // 没有发音就手动拼接一个发音
                ret.data.usspeech = ret.data.word + '&type=2'
            } else {
                this.audio.src = 'https://dict.youdao.com/dictvoice?audio=' + ret.data.usspeech
            }
            await this.audio.play()
        },
        async click_voice() {
            if (this.word_detail.usspeech.length === 0) {
                // 没有发音就手动拼接一个发音
                this.word_detail.usspeech = this.word_detail.word + '&type=2'
            } else {
                this.audio.src = 'https://dict.youdao.com/dictvoice?audio=' + this.word_detail.usspeech
            }
            await this.audio.play()
        }
    },
    props: {
        word_id: {
            type: Number,
            required: true
        }
    }
}
</script>
<style scoped>
.child {
    width: 50px;
    height: 35px;
    background: #d0d0d0;
    border-radius: 4px;
}

.fixed-bottom {
    position: fixed;
    bottom: 0;
    width: 100%;
}
</style>
