USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_CountyInfo]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_CountyInfo](
	[VGProductID] [int] NOT NULL,
	[CountyName] [varchar](50) NULL,
	[CountyWebSite] [varchar](50) NULL,
	[Title] [varchar](70) NULL,
	[Slogan] [varchar](80) NULL,
	[TaxCertTableName] [varchar](30) NULL,
	[CSSFile] [varchar](30) NULL,
	[HostAddress] [varchar](50) NULL,
	[TaxYear] [int] NULL,
	[TaxViewTableName] [varchar](50) NULL,
	[AuctionLiveDate] [smalldatetime] NULL,
	[PropertyLink] [varchar](500) NULL,
	[ExemptTable] [varchar](50) NULL,
	[RequestorName] [varchar](50) NULL,
	[QueueStartID] [int] NULL,
	[LastOnlineDepositDate] [smalldatetime] NULL,
	[AuctionResultsStatus] [int] NULL,
	[SiteEnabled] [bit] NULL,
	[MobileEnabled] [bit] NULL,
	[MobileTheme] [varchar](20) NULL,
 CONSTRAINT [PK_vg_CountyInfo] PRIMARY KEY CLUSTERED 
(
	[VGProductID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[vg_CountyInfo] ADD  CONSTRAINT [DF_vg_CountyInfo_SiteEnabled]  DEFAULT ((1)) FOR [SiteEnabled]
GO
